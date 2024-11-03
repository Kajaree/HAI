import json
from openai import OpenAI

class GPTAgent:
    def __init__(self, file_paths):
      self.client = None
      self.assistant = None
      self.vector_store = None
      self.isConfigUpdated = False
      self.__initialize(file_paths)


    def __initialize(self, file_paths):
      credentials = None
      # read the credentials from credentials.json
      with open('credentials.json') as creds_file:
         credentials = json.load(creds_file)

      # define the OpenAI Client
      self.client = OpenAI(
                organization=credentials['organization'],
                project=credentials['project'],
                api_key=credentials['api_key']
              )
      assistant_config = {}
      # read the assistant id and vector store id
      with open('config.json') as config_file:
         assistant_config = json.load(config_file)
      self.__initialize_assistant(assistant_config['assistant_id'])
      self.__initialize_vector_store(assistant_config['vector_store_id'], file_paths)
      # update config file if a new assistant and/or vector store is created
      if self.isConfigUpdated:
        self.__update_config_file()        

    def __initialize_assistant(self, assistant_id):
      # if an assistant exists with the provided assistant id, reuse it
      # else, create a new one
      try:
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
      except:
        print('No Research assistant found. Creating one.')
        self.assistant = self.client.beta.assistants.create(
                        name="Research Assistant",
                        instructions="You are an expert research assistant. Use your knowledge base to answer questions about research papers.",
                        model="gpt-4o-mini",
                        tools=[{"type": "file_search"}],
                      )
        self.isConfigUpdated = True

        
    def __initialize_vector_store(self, vector_store_id, file_paths):
      # if a vector store exists with the provided vector store id, reuse it
      # else, create a new one
      try:
        self.vector_store = self.client.beta.vector_stores.retrieve(vector_store_id=vector_store_id)
      except:
        print('No papers in the database. Uploading them now.')
        self.vector_store = self.client.beta.vector_stores.create(name="Research Papers")
        
        # Ready the files for upload to OpenAI
        file_streams = [open(path, "rb") for path in file_paths]
          
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=file_streams
        )
          
        # Print the status to see the result of this operation.
        print(file_batch.status)
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
        )
        self.isConfigUpdated = True
       
    def __update_config_file(self):
      new_assistant_config = {'assistant_id': self.assistant.id, 'vector_store_id': self.vector_store.id}
      # Writing to config.json
      with open("config.json", "w") as outfile:
        outfile.write(json.dumps(new_assistant_config, indent=4))
       
    def askAgent(self, prompt):
      # use the assistant to answer queries based on prompts provided
      if not prompt:
        print('Please provide valid query and try again')
        return
      
      thread = self.client.beta.threads.create(
        messages=[{
              "role": "user",
              "content": prompt
            }],
        tool_resources={
          "file_search": {
              "vector_store_ids": [self.vector_store.id]
          }
        }
      )

      run = self.client.beta.threads.runs.create_and_poll(
          thread_id=thread.id, assistant_id=self.assistant.id
      )

      messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

      summary = messages[0].content[0].text
      self.client.beta.threads.delete(thread_id=thread.id)
      
      print(summary.value)
