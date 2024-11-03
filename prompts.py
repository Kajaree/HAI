summary_prompts = ['Specify whether this paper is focused on a specific industry, task or a broader, conceptual scope.', 
           'Identify the main research question and summarize the key findings of this paper.', 
           'Human vs. AI: Highlight any comparisons of comparative advantages between humans and AI, including condition-based results or scenarios where one outperforms the other mentioned in this paper.',
           'Human + AI Collaboration: Indicate the type of collaboration discussed, such as the roles of human and AI, the sequences of actions of human and AI taken in the process, and so on mentioned in this paper.',
           'Classify the method of this paper as one of the following: Conceptual/Case Study, Modeling: Either Stylized Modeling or Operations Research (OR) Model, Empirical Study: Lab/Field Experiment or Secondary Data Analysis',
           'Identify the primary contribution of this paper, categorizing it as theoretical, managerial, or methodological.',
           'Summarize what this paper states about future research directions or the limitations of its findings.']

review_prompts = ['Generate summaries of these articles in the specified format.',
                  'Compile the summaries into coherent paragraphs that discuss how the research in these areas is connected, identifying common themes, trends, and potential future directions.',
                  'Provide a reference list for all retrieved articles, formatted according to standard academic citation styles.']

category_prompt = ['Among the 30 papers, just tell me how many are conceptual studies in one sentence.', 
                   'Among the 30 papers, just tell me how many are modeling studies (either stylized or OR models) in one sentence.', 
                   'Among the 30 papers, just tell me how many are empirical studies in one sentence.', 
                   'Of the empirical studies, exactly how many are experiments, and how many use secondary data analysis. Please provide the exact count for each type of research.' ]