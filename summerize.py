import os
from GPTAgent import GPTAgent
from prompts import summary_prompt, review_prompt, category_prompt

paper_dir = "papers"
paper_list = os.listdir(paper_dir)
file_list = [os.path.join(paper_dir, path_to_paper) for path_to_paper in paper_list]
summarize_tool = GPTAgent(file_list)
author = 'Gnewuch'
year = '2023'
prompts = f'Print the title of the paper which has {author} as its first author and was published in {year}.'
summarize_tool.askAgent(prompts + summary_prompt)

user_prompt = input('Please write your query about the papers and our tool will try to answer. Else we will ask for a generic review\n')
if not user_prompt:
  user_prompt = 'Please summarize empirical research about human VS AI'
summarize_tool.askAgent(user_prompt + review_prompt)
summarize_tool.askAgent(category_prompt)