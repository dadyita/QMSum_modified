import re
import json
import openai
import random
import threading

openai.api_key = "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"
prompt_count = 4


class PromptTest:
    @staticmethod
    def query_prompt(query_list, prompt_index):
        prompt = ['''There is a list in json format consisting of multiple queries.
    Extract keywords from each query and regenerate a new query that is a coherent question including all keywords from all original queries.
    
    Here is an example you can follow.
    Query list:
    [
    "Summarize the discussion about the name chosen of the product.",
    "Summarize the decision of the discussion on the name chosen of the product.",
    "Summarize the group's decision on colour and logo of the product."
    ]
    
    New Query:
    Summarize the final decision on the name, color, and logo of the product.
    
    Now process the following example:''',
                  '''There is a list in json format consisting of multiple queries.
    Use keywords of all queries to regenerate a new query. Requires the new query to be able to find the content that all original queries query. New query should be a coherent question.
    
    Here is an example you can follow.
    Query list:
    [
    "Summarize the discussion about the name chosen of the product.",
    "Summarize the decision of the discussion on the name chosen of the product.",
    "Summarize the group's decision on colour and logo of the product."
    ]
    
    New Query:
    Summarize the final decision on the name, color, and logo of the product.
    
    Now process the following example:
    ''',
                  '''The input is a list in json format consisting of multiple queries.
    Form a new query based on all original queries as output. It is required not to lose the original information. The new query can search for information that the original query searched for. The new query needs to be free of any unnecessary repetitions or words. New query should be a coherent question.
    
    Here is an example you can follow.
    Query list:
    [
    "Summarize the discussion about the name chosen of the product.",
    "Summarize the decision of the discussion on the name chosen of the product.",
    "Summarize the group's decision on colour and logo of the product."
    ]
    
    New Query:
    Summarize the final decision on the name, color, and logo of the product.
    
    Now process the following example:''',
                  '''The input is a list in json format consisting of multiple queries.
    Form a new query based on all original queries as output. It is required not to lose the original information. The new query can search for information that the original query searched for. The new query needs to be free of any unnecessary repetitions or words. New query should be a coherent question. The new query needs to meet the following four criteria:Relevance, Consistency, Fluency, Coherence. Here are the explanation of the criteria
    Relevance: The new query needs to capture the key points of the query list.
    Consistency:the facts in the text are consistent with the facts in the original query lists.
    Fluency:The query is well-written and grammatically correct.
    Coherence: Fit together and sound natural.
    
    Here is an example you can follow.
    Query list:
    [
    "Summarize the discussion about the name chosen of the product.",
    "Summarize the decision of the discussion on the name chosen of the product.",
    "Summarize the group's decision on colour and logo of the product."
    ]
    
    New Query:
    Summarize the final decision on the name, color, and logo of the product.
    
    Now process the following example:''',
                  '''The input is a list in json format consisting of multiple queries.
    Form a new query based on all original queries as output. It is required not to lose the original information. The new query can search for information that the original query searched for. 
    The new query needs to be free of any unnecessary repetitions or words. New query should be a coherent question. 
    The new query needs to meet the following four criteria:Relevance, Consistency, Fluency, Coherence. Here is the explanation of the criteria.
    Relevance: The new query needs to capture the key points of the query list.
    Consistency:the facts in the text are consistent with the facts in the original query lists.
    Fluency:The query is well-written and grammatically correct.
    Coherence: Fit together and sound natural.
    
    Here is an example you can follow.
    Query list:
    [
    "Summarize the discussion about the name chosen of the product.",
    "Summarize the decision of the discussion on the name chosen of the product.",
    "Summarize the group's decision on colour and logo of the product."
    ]
    
    New Query:
    Summarize the final decision on the name, color, and logo of the product.
    
    Now process the following example:
    ''']
        # assistant=""
        user = 'Query list:\n' + query_list
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": prompt[prompt_index]},
                # {"role": "user", "content": user1},
                # {"role": "assistant", "content": assistant1},
                {"role": "user", "content": user}
            ],
            temperature=0,
        )
        result_query = response['choices'][0]['message']['content']
        return result_query

    @staticmethod
    def answer_prompt(answer_list):
        prompt = '''The input is a list in json format consisting of multiple sentences.
    Form a summary based on all original sentences as output. It is required not to lose the original information. 
    The new summary needs to be free of any unnecessary repetitions or words. New summary should be a coherent sentence. 
    The summary needs to meet the following four criteria:Relevance, Consistency, Fluency, Coherence. Here is the explanation of the criteria.
    Relevance: The summary needs to capture the key points of the sentences list.
    Consistency: The facts in the text are consistent with the facts in the original sentences lists.
    Fluency:The summary is well-written and grammatically correct.
    Coherence: Fit together and sound natural.
    
    Here is an example you can follow.
    Sentence list:
    [
    "The corporate colour and design are recommended to be used on the product. The remote could be in different colours such as pink or banana yellow and shapes such as a fun shape like animal shapes or a comfortable shape that fits the hand but no sharp projections, lest a child plays with it. The idea of buttons with various shapes such as a triangle for volume and square for channels was considered. Everyone agreed that the text on the remote should be clear and the remote should be compact.",
    "The group talked about the material and they found it would be hard to balance the budget and the quality. In order to save the cost and ensure satisfying user experience, the Project Manager decided to choose high-quality recycled plastic as the material. But in terms of the battery, he would pay a lot to equip the remote with a cutting-edge lithium battery.",
    "In terms of putting fashion into the electronics, this is both their slogan and their design target. Apart from the company colour of black and red, the Project Manager came up with the idea of providing skins for the users. But the members were not in favour of this idea for that the work would be huge, at the same time, they were inspired to add the logo on the boot-up screen and introduce a dormant mode because most people do not want the remote to be flashing when the TV is on.",
    "There were two reasons. The first was that the unit price of each remote control was relatively high (twenty-five Euros). Therefore, in order to increase customers' willingness to spend so much money on one single remote control, the features must be satisfying and good enough. The second was the competition since there were other TV remote controls in the market. The new TV remote controls shall be special and different from the rest so as to attract customers."
    ]
    
    Summary:
    The company emphasizes incorporating its corporate colours and design into the product, suggesting potential remote designs in varying colors like pink and banana yellow, possibly with fun shapes such as animals. Functionality suggestions include uniquely shaped buttons like triangles for volume and squares for channels, and everyone concurred on the clarity of the text and a compact size. Given budget constraints and quality considerations, the decision was made to use high-quality recycled plastic for the remote, paired with a premium lithium battery. While the company's motto revolves around infusing fashion into electronics, and initial ideas of user-customizable skins were rejected, the incorporation of the logo on the boot-up screen and a dormant mode were agreed upon, as customers generally dislike flashing remotes. The drive behind these design choices was twofold: the relatively high unit price of twenty-five Euros warranted feature-rich and satisfactory remotes, and the need to distinguish the product in a competitive market.
    
    Now process the following example:'''
        user = 'Sentence list:\n' + answer_list
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": prompt},
                # {"role": "user", "content": user1},
                # {"role": "assistant", "content": assistant1},
                {"role": "user", "content": user}
            ],
            temperature=0,
        )
        result_query = response['choices'][0]['message']['content']
        return result_query

    @staticmethod
    def evaluate(str_list, merge, index):
        # Index 0 means query
        # Index 1 means answer
        system = ['''Imagine you are a human annotator now. You will evaluate the quality of one summary query based on a given json format query list and explain why the score is given in every single dimension in detail. Please follow these steps:
    1. Carefully read every query in the query list, be aware of the information they contain and analyze their key points and important aspects.
    2. Read the summary query carefully and understand its content.
    3. Rate the summary query on four dimensions: relevance, consistency, fluency, and coherence. You should rate on a scale from 1 (worst) to 5 (best). Note that scores are integers . Please remember to rate each dimension separately and strictly by definition.
    
    Relevance: The rating measures how well the new query captures the key points of the query list. Consider whether all and only the important aspects are contained in the new query without any unnecessary repetitions. Note that 1 point indicates that the new query only includes some unrelated and insignificant content without any important information from the source query list. You could penalize summaries which contained redundancies and excess information by giving a relative low score in this dimension.
    
    Consistency: The rating measures whether the facts in the text are consistent with the facts in the original query lists. Consider whether the new query does reproduce all facts accurately and does not make up untrue information. Note that 1 point indicates the new query doesn't have any fact entailed by the source query list. You could penalize summaries that contained hallucinated facts by giving a relative low score in this dimension.
    
    Fluency: This rating measures the quality of individual sentences, whether they are well-written and grammatically correct. Consider the quality of individual sentences. If you find formatting problems, capitalization errors or obviously ungrammatical sentences (e.g., fragments, missing components) that make the text difficult to read, you could penalize the new query by giving a relative low score in this dimension.
    
    Coherence: The rating measures the quality of all sentences collectively, to fit together and sound natural. Consider the quality of the new query as a whole. Note that 1 point indicates should just be a heap of related information. You could penalize the new query that is not a coherent body of information from the source query list by giving a relative low score in this dimension.
    
    Here is an example you can follow.
    Query list:
    [
    "Summarize the discussion about the name chosen of the product.",
    "Summarize the decision of the discussion on the name chosen of the product.",
    "Summarize the group's decision on colour and logo of the product."
    ]
    
    Summary query:
    Summarize the final decision on the name, color, and logo of the product.
    
    Evaluation Form (score and explain the four scores based on four dimensions)：
    -Relevance: 5
    -Explanation: The summary query captures all the key points from the query list. It includes the discussion about the name chosen, the decision on the name chosen, and the group's decision on the color and logo of the product. There are no unnecessary repetitions or unrelated content.
    
    -Consistency: 5
    -Explanation: The summary query accurately reproduces the facts from the query list. It mentions the final decision on the name, color, and logo of the product, which aligns with the discussions and decisions mentioned in the query list. There are no made-up or untrue information.
    
    -Fluency: 5
    -Explanation: The summary query is well-written and grammatically correct. The sentences are clear and easy to understand. 
    
    -Coherence: 5
    -Explanation: The summary query forms a coherent body of information from the query list. It combines the discussions and decisions about the name, color, and logo of the product into a single summary. The information flows logically and there are no abrupt transitions or disjointed sentences.
    
    Now rate the following example:
    ''',
                  '''Imagine you are a human annotator now. You will evaluate the quality of one summary based on a given json format sentence list and explain why the score is given in every single dimension in detail. Please follow these steps:
    1. Carefully read every sentence in the sentence list, be aware of the information they contain and analyze their key points and important aspects.
    2. Read the summary carefully and understand its content.
    3. Rate the summary on four dimensions: relevance, consistency, fluency, and coherence. You should rate on a scale from 1 (worst) to 5 (best). Note that scores are integers. Please remember to rate each dimension separately and strictly by definition.
    
    Relevance: The rating measures how well the summary captures the key points of the sentence list. Consider whether all and only the important aspects are contained in the summary without any unnecessary repetitions. Note that 1 point indicates that the summary only includes some unrelated and insignificant content without any important information from the source sentence list. You could penalize summaries which contained redundancies and excess information by giving a relative low score in this dimension.
    
    Consistency: The rating measures whether the facts in the text are consistent with the facts in the original sentence lists. Consider whether the summary does reproduce all facts accurately and does not make up untrue information. Note that 1 point indicates the summary doesn't have any fact entailed by the source sentence list. You could penalize summaries that contained hallucinated facts by giving a relative low score in this dimension.
    
    Fluency: This rating measures the quality of individual sentences, whether they are well-written and grammatically correct. Consider the quality of individual sentences. If you find formatting problems, capitalization errors or obviously ungrammatical sentences (e.g., fragments, missing components) that make the text difficult to read, you could penalize the summary by giving a relatively low score in this dimension.
    
    Coherence: The rating measures the quality of all sentences collectively, to fit together and sound natural. Consider the quality of the summary as a whole. Note that 1 point indicates should just be a heap of related information. You could penalize the summary that is not a coherent body of information from the source sentence list by giving a relatively low score in this dimension.
    
    Here is an example you can follow.
    Sentence list:
    ["According to the user interface designer, to implement this function, the users should press a button to start the program and type in their favourite channels. The project manager liked this idea and the marketing thought it would be another great market tool. In terms of the cost, the project manager believed it wouldn't be too expensive because they could come up with a partnership to produce that quite cheaply, but the marketing held that the technology was available through their own service. Furthermore, this function must be accompanied by a mode switch and an indicator.", "Marketing thought they should design a remote control for television only due to the issue of advancement. User Interface supposed that it would be nice to have playing and recording and stop buttons on remote controls for the video recorder as well, but he didn't know if that worked technologically. Industrial Designer agreed to define the object of remote control, and he proposed that it would be simpler if it's just for television because there were fewer buttons, which would benefit older people or people that weren't very co-ordinated hand-eye.", "Industrial Designer expressed initial working design about remote control. User Interface suggested that remote control should be user friendly with not too much but clear buttons. Marketing showed us data about functional requirement remote control. Project Manager said that the new requirement about remote control was teletext should be paid less attention as it was outdated. Future customers' age should be focused on forty plus and new design should include corporate colour and slogan.", "Project Manager said that remote control should only work with TV. Marketing thought the basics should be volume, channel and one till two zero numbers. Users Interface suggested remote control should with a button you can change from one number to two numbers.", "The User Interface proposed to build a stand-alone one, which can be different from any other devices. The Project Manager then added that it might be better with more useful functions like changing the faces. Marketing came up with the idea of making it be functional for other devices as well, just including everything in this remote control.", "The project manager wanted to remove the kinetic function as the manager thought it would be a desirable cost reduction. However, the industrial designer did not agree with the project manager because the designer thought it would be a good marketing promotion as people would think that remote controls with kinetic function are cool. Since they still wanted the price to remain on the same level, they decided to adapt the control into a flat one so as to minimize the cost."]
    
    Summary:
    The user interface designer suggested a function where users can start a program and input their favorite channels by pressing a button, which was well-received by the project manager and marketing team as a potential market tool. The project manager believed the cost would be manageable through partnerships, while marketing argued that the technology was already available through their own service. This function would require a mode switch and an indicator. Marketing proposed designing a remote control specifically for television, while the user interface designer suggested adding buttons for playing, recording, and stopping on video recorders, although unsure of the technological feasibility. The industrial designer agreed that a simpler remote control for television would benefit older or less coordinated users. The initial working design of the remote control was presented, with a focus on user-friendliness and clear buttons. The project manager emphasized that teletext should be given less attention as it was outdated, and the target customers should be forty-plus, incorporating the corporate color and slogan. The remote control should only work with TV, with basic functions such as volume, channel, and one to two-digit numbers. The user interface proposed a stand-alone remote control with unique features, while the project manager suggested adding more useful functions like changing faces. Marketing suggested making the remote control functional for other devices as well. There was a disagreement between the project manager and industrial designer regarding the removal of the kinetic function, with the designer seeing it as a cool marketing promotion. To maintain the price level, they decided to adapt the control into a flat design to minimize costs.
    
    Evaluation Form (score and explain the four scores based on four dimensions)：
    -Relevance: 4
    -Explanation: The summary effectively captures the main points from the sentence list. It touches upon the button function proposed by the User Interface designer, the stance of the project manager and marketing team on its implementation, and the thoughts around the design and functionality of the remote control. The summary also captures the disagreement on the kinetic function and the cost implications.However, there are some minor points from the sentence list that aren't covered. For instance, the part about the future customers' age being focused on forty plus and including the corporate color and slogan wasn't as emphasized.
    
    -Consistency: 5
    -Explanation: The summary stays consistent with the information provided in the sentence list. There is no hallucinated or untrue information added in the summary. The facts mentioned in the summary accurately reflect the content of the sentence list.
    
    -Fluency: 5
    -Explanation: The summary is well-written, with grammatically correct sentences. There are no apparent formatting issues, capitalization errors, or fragmented sentences. The text is easy to read and understand.
    
    -Coherence: 5
    -Explanation: The summary is coherent, presenting the information in a logical flow. It starts with the button function proposed, moves to the design and functionality discussions, and then ends with the disagreement on the kinetic function and the resultant decision. The transitions between topics are smooth, and the summary reads as a cohesive piece.
    
    Now rate the following example:''']
        # assistant=""
        user = ["Query list:\n" + str_list + "\n\nSummary query:\n" + merge,
                "Sentence list:\n" + str_list + "\n\nSummary:\n" + merge]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": system[index]},
                # {"role": "user", "content": user1},
                # {"role": "assistant", "content": assistant1},
                {"role": "user", "content": user[index]}
            ],
            temperature=0,
        )
        result_summary = response['choices'][0]['message']['content']
        return result_summary

    @staticmethod
    def random_select(my_dict, count):
        keys = random.sample(list(my_dict.keys()), count)
        selected_items = {key: my_dict[key] for key in keys}
        return selected_items

    @staticmethod
    def select_test_data():
        # Path
        specific_queries_file_path = './clustered_queries.json'

        # Reading the content of the new file
        with open(specific_queries_file_path, 'r') as file:
            specific_queries_content = json.load(file)

        # Extracting the queries from the specific_queries_content
        # queries = {key: [item['query'] for item in value] for key, value in specific_queries_content.items()}
        # summaries = {key: [item['answer'] for item in value] for key, value in specific_queries_content.items()}

        # Random select
        select = PromptTest.random_select(specific_queries_content, 20)
        select_queries = {key: [item['query'] for item in value] for key, value in select.items()}
        select_summaries = {key: [item['answer'] for item in value] for key, value in select.items()}

        # Save selected to evaluate
        with open('queries_selected.json', 'w') as f:
            temp = json.dumps(select_queries)
            f.write(temp)

        with open('summaries_selected.json', 'w') as f:
            temp = json.dumps(select_summaries)
            f.write(temp)

    @staticmethod
    def run_prompt():
        # Load data
        with open('DataSet/queries_selected.json', 'r') as f:
            select_queries = json.load(f)

        for i in range(prompt_count):
            # Result list
            result_queries = {}
            for index, _list in select_queries.items():
                str_list = json.dumps(_list)
                query = PromptTest.query_prompt(str_list, i)

                # Remove 'New Query:\n'
                if query.startswith('New Query:\n'):
                    query = query.replace('New Query:\n', '')
                result_queries[index] = query

                # Print query
                print(str(i) + ':')
                print(query)
                print()

            with open('DataSet/queries_prompt' + str(i) + '.json', 'w') as f:
                temp = json.dumps(result_queries)
                f.write(temp)

    @staticmethod
    def run_summary():
        with open('DataSet/summaries_selected.json', 'r') as f:
            select_summaries = json.load(f)

        # Result list
        result_summaries = {}
        for index, _list in select_summaries.items():
            str_list = json.dumps(_list)
            summary = PromptTest.answer_prompt(str_list)

            # Remove 'Summary:\n'
            if summary.startswith('Summary:\n'):
                summary = summary.replace('Summary:\n', '')
            result_summaries[index] = summary

            # Print Summary
            print(summary)
            print()

        with open('DataSet/summaries_prompt.json', 'w') as f:
            temp = json.dumps(result_summaries)
            f.write(temp)

    @staticmethod
    def thread_evaluate(i):
        # Load data
        with open('DataSet/queries_selected.json', 'r') as f:
            select_queries = json.load(f)

        # Load generate summary
        with open('DataSet/queries_prompt' + str(i) + '.json', 'r') as f:
            queries = json.load(f)

        # Result list
        result_evaluation = {}
        for index, query_list in select_queries.items():
            # Get merge query
            query = queries[index]
            # Convert it to string
            str_query_list = json.dumps(query_list)
            # Evaluate
            evaluation = PromptTest.evaluate(str_query_list, query, 0)
            # Add to result
            result_evaluation[index] = evaluation

            # Print query
            print(str(i) + ':')
            print(evaluation)
            print()

        with open('DataSet/queries_evaluation' + str(i) + '.json', 'w') as f:
            temp = json.dumps(result_evaluation)
            f.write(temp)

    @staticmethod
    def run_query_evaluate():
        thread_list = []
        for i in range(prompt_count):
            t = threading.Thread(target=PromptTest.thread_evaluate, args=(i,))
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()

    @staticmethod
    def run_summary_evaluate():
        # Load data
        with open('DataSet/summaries_selected.json', 'r') as f:
            select_queries = json.load(f)

        # Load summary
        with open('DataSet/summaries_prompt.json', 'r') as f:
            queries = json.load(f)

        # Result list
        result_evaluation = {}
        for index, query_list in select_queries.items():
            # Get merge query
            query = queries[index]
            # Convert it to string
            str_query_list = json.dumps(query_list)
            # Evaluate
            evaluation = PromptTest.evaluate(str_query_list, query, 1)
            # Add to result
            result_evaluation[index] = evaluation

            # Print query
            print(evaluation)
            print()

        with open('DataSet/summaries_evaluation.json', 'w') as f:
            temp = json.dumps(result_evaluation)
            f.write(temp)

    @staticmethod
    def get_num(string, index):
        # 使用正则表达式匹配"Fluency"后面的数字
        pattens = [r"Relevance:\s+(\d+)", r"Consistency:\s+(\d+)", r"Fluency:\s+(\d+)", r"Coherence:\s+(\d+)"]
        match = re.search(pattens[index], string)

        if match:
            fluency_score = int(match.group(1))
        else:
            fluency_score = -1
        return fluency_score

    @staticmethod
    def calculate_average():
        for i in range(prompt_count):
            # with open('DataSet/queries_evaluation' + str(i) + '.json', 'r') as f:
            with open('DataSet/summaries_evaluation.json', 'r') as f:
                data = json.load(f)
                scores = [0, 0, 0, 0]
                for index, string in data.items():
                    for j in range(4):
                        scores[j] += PromptTest.get_num(string, j)
                scores = [item / 20 for item in scores]
                print(scores)


def get_data():
    temp = [1, 1, 1]
    with open('./DataSet/Academic/clustered_queries.json', 'r') as f:
        temp[0] = json.load(f)
    with open('./DataSet/Product/clustered_queries.json', 'r') as f:
        temp[1] = json.load(f)
    with open('./DataSet/Committee/clustered_queries.json', 'r') as f:
        temp[2] = json.load(f)
    return temp


def thread_process_cluster(cluster_list, i):
    result = {}

    for index, cluster in cluster_list.items():
        # Get query_list, answer_list from cluster_list
        queries = [item['query'] for item in cluster]
        answers = [item['answer'] for item in cluster]
        # Get merge_query, merge_answer
        merge_query = PromptTest.query_prompt(json.dumps(queries), 3)
        merge_answer = PromptTest.answer_prompt(json.dumps(answers))

        # Remove 'New Query:\n'
        if merge_query.startswith('New Query:\n'):
            merge_query = merge_query.replace('New Query:\n', '')

        result[index] = {"query": merge_query, "answer": merge_answer}
        print(str(i) + ':')
        print(json.dumps(result, indent=4))

    with open('merged_queries' + str(i) + '.json', 'w') as f:
        temp = json.dumps(result)
        f.write(temp)


def main():
    file_lists = get_data()
    t_list = []
    for i in range(3):
        t = threading.Thread(target=thread_process_cluster, args=(file_lists[i], i))
        t_list.append(t)
        t.start()

    for t in t_list:
        t.join()


if __name__ == '__main__':
    main()

