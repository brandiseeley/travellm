# Time Travel LLM Project Writeup

📹 Loom Video recording: https://www.loom.com/share/38ef280e48014ccc940c6c994e802573?sid=9dc9dd41-ae0a-4059-9e75-156f6cb118e0

## Task 1: Defining your Problem and Audience

### Problem Description

✅ Educators and content creators struggle to access and understand authentic historical perspectives from specific time periods because they lack a conversational interface that can provide contextually accurate responses based on historical newspaper articles and primary sources from those eras.

### Why This is a Problem for Your Specific User

✅ The primary users of this system are educators and content creators who need to engage their audiences with authentic historical perspectives. Teachers seeking to bring history to life for their students, content creators looking to tell compelling stories from the past, and educational content developers all face significant barriers when trying to access historical viewpoints. Currently, they must manually search through digitized newspaper archives, read through dense historical texts, and piece together context from multiple sources - a time-consuming and often overwhelming process that requires significant historical research expertise.

This problem is particularly acute because understanding how people thought about and discussed events in their own time is crucial for creating engaging, accurate historical content. Traditional search engines and modern AI systems provide contemporary perspectives rather than authentic historical viewpoints, making it difficult for educators and creators to truly "step back in time" and experience the world as it was understood in different historical periods. The Time Travel LLM solves this by creating an immersive, conversational experience that responds as someone from a specific historical era would, using actual historical sources as the foundation for its responses. 

## Task 2: Propose a Solution

### Proposed Solution

✅ The Time Travel LLM creates an immersive conversational interface that allows users to interact with historical perspectives from any time period. Users simply type questions into a clean, intuitive web interface, and the system responds as someone from that historical era would, using authentic language, knowledge, and viewpoints from the time. The experience feels like having a conversation with a knowledgeable person from the past who can discuss current events, medical practices, social customs, and daily life as they were understood in that period.

The system works by combining a retrieval-augmented generation (RAG) approach with historical newspaper articles and primary sources. When a user asks a question, the system intelligently searches through digitized historical documents to find relevant context, then generates responses that reflect the authentic voice and knowledge of people from that era. The interface is designed to be simple and accessible - just a question input and response area - but the underlying system provides rich, contextually accurate historical perspectives that educators and content creators can use to bring history to life.

### ✅ Tooling Choices

**LLM**: OpenAI GPT-4 for generating historically accurate responses, chosen for its strong reasoning capabilities and ability to adopt different personas and writing styles.

**Embedding Model**: OpenAI text-embedding-3-small for creating vector representations of historical documents, selected for its high performance and cost-effectiveness in semantic search tasks.

**Orchestration**: LangGraph for managing the multi-step RAG workflow, chosen for its flexibility in creating complex reasoning chains and agent workflows.

**Vector Database**: PostgreSQL with PGVector extension for storing and retrieving historical document embeddings, selected for its robust performance, ACID compliance, and enterprise-grade reliability.

**Monitoring**: LangSmith for tracing and debugging the RAG pipeline, chosen for its seamless integration with LangChain/LangGraph and comprehensive observability features.

**Evaluation**: RAGAS for automated evaluation of retrieval and generation quality, selected for its specialized metrics for RAG system performance.

**User Interface**: Flask web application with simple HTML/CSS, chosen for rapid prototyping and easy deployment.

**Serving & Inference**: Local deployment with Flask development server, selected for simplicity during prototyping phase.

### Agent Usage

The system uses agentic reasoning primarily for intelligent document retrieval when users ask about specific topics or events. The LLM uses function calling to dynamically determine the most relevant search terms and then searches both local document collections and external historical databases like the Library of Congress to find additional context. This allows the system to supplement its local knowledge with broader historical sources when needed, ensuring more comprehensive and accurate responses about specific historical topics.

## Task 3: Dealing with the Data

### ✅ Data Sources and External APIs

**Primary Historical Data**: The system uses the American Stories dataset from Harvard, specifically articles from 1861, which provides digitized newspaper articles with rich metadata including newspaper names, dates, and full article text. This serves as the core knowledge base for generating authentic 1861-era responses. Other dates could certainly be used, but 1861 has been chosen for simplicity in protoyping, and a rich, tumultuous time in history.

**Library of Congress API**: The system integrates with the Library of Congress Chronicling America collection through their REST API to supplement local knowledge. This allows the system to search for additional historical articles when users ask about specific topics not covered in the local dataset, providing broader historical context and more comprehensive responses.

**OpenAI APIs**: The system uses OpenAI's text-embedding-3-small model for creating vector representations of historical documents and GPT-4 for generating responses, enabling semantic search and contextually appropriate historical dialogue.

### ✅ Default Chunking Strategy

The system uses a `RecursiveCharacterTextSplitter` with a chunk size of 750 tokens and no overlap between chunks. This decision was made mostly to provide a starting point before investigating other strategies. Having an end-to-end application working to be able to make decisions based on evaluations was important to me.

## Task 4: Building a Quick End-to-End Agentic RAG Prototype

✅ See `README.md` for instructions on running application locally.

## Task 5: Creating a Golden Test Data Set

- ✅ Golden test set with 50 examples can be found in `data/sythetic_dataset.json`

### Results

<details>
<summary>Full Results</summary>

|user_input             |retrieved_contexts     |response               |reference              |faithfulness       |answer_relevancy  |llm_context_precision_with_reference|context_recall     |
|-----------------------|-----------------------|-----------------------|-----------------------|-------------------|------------------|------------------------------------|-------------------|
|What are the benefit...|["RADwAY's RESovATIS...|Ah, you've come at a...|RADwAY's RESovATISG ...|0.9090909090909091 |0.0               |0.9999999999                        |1.0                |
|Wut is the location ...|["Presbyteriah-Liber...|Ah, welcome to our f...|St. Lssis is located...|0.0                |0.0               |0.0                                 |0.0                |
|What significant eve...|["He Is SUCCEEDED By...|Ah, I see you’ve hea...|Major Wright, who is...|0.5555555555555556 |0.8625889175829963|0.9166666666361111                  |1.0                |
|What role did S.Sava...|['APPOINTMENTS IS TH...|Ah, I see you are cu...|Col. Hardee of S.Sav...|1.0                |0.0               |0.9999999999                        |1.0                |
|What was the reactio...|["sseldIers In Peace...|Ah, you’ve come just...|The citizens in the ...|1.0                |0.940837356471071 |0.699999999965                      |0.3333333333333333 |
|What role does the C...|["STATE OF MICHIGAN-...|Ah, welcome to Dowag...|The Cass County Repu...|0.7058823529411765 |0.9790249702491177|0.94999999997625                    |1.0                |
|How did North Caroli...|['The lower branch O...|Well, friend, it’s a...|The lower branch of ...|0.8461538461538461 |0.0               |0.99999999995                       |1.0                |
|Who is Harrison Weir...|['THE POETRY OF NATU...|Ah, you’ve asked abo...|Harrison Weir is kno...|0.16666666666666666|0.0               |0.9999999999                        |1.0                |
|Who is J. Ii. q. JQh...|['JEFF Thompson A VI...|I reckon you've got ...|J. Ii. q. JQhhbON is...|0.8666666666666667 |0.0               |0.0                                 |0.0                |
|What happened on Feb...|["W y ~\n\n\nARSENAL...|Well, my friend, I c...|On Feb. II, 1860, th...|0.9333333333333333 |0.0               |0.0                                 |0.0                |
|Wht is the number of...|['transfers, time an...|Well, it seems there...|The context mentions...|0.8333333333333334 |0.0               |0.99999999998                       |1.0                |
|Can you provide an o...|['HISTORY OF ENGLAND...|Ah, I see you’re cur...|The HISTORY OF ENGLA...|0.3                |0.0               |0.9999999999                        |1.0                |
|What notable agricul...|['A sweet potato was...|Ah, I see you've an ...|A sweet potato that ...|0.18181818181818182|0.0               |0.9999999999                        |1.0                |
|What can you tell me...|['From the Examiner,...|Ah, greetings! I see...|In a letter dated Ja...|0.3333333333333333 |0.0               |0.99999999998                       |0.0                |
|What is the Arctic L...|["b r a q G9S\n\n\nA...|Ah, welcome, friend!...|The Arctic Liniment ...|0.5                |0.0               |0.999999999975                      |1.0                |
|What is the focus of...|['Progress of Slaver...|Ah, greetings! You’v...|George M. Weston's w...|0.7647058823529411 |0.0               |0.99999999995                       |1.0                |
|What is near the Cit...|["Nashville, Tenness...|Ah, so you're askin'...|The City Hotel is ne...|0.35294117647058826|0.9011770066957151|0.0                                 |0.0                |
|What role did Peruvi...|['Tit. oil, CANT com...|Well, let me tell yo...|Peruvian Bark was no...|0.7368421052631579 |0.9125613747765469|0.9999999999666667                  |1.0                |
|What were the circum...|['War GsSrR,t Scor1 ...|Ah, welcome to Terre...|General Scott will v...|0.6470588235294118 |0.0               |0.36666666664833336                 |0.5                |
|What was the signifi...|["HEa are unwilling ...|Ah, welcome to our f...|The public meeting i...|0.875              |0.0               |0.8874999999778125                  |1.0                |
|How did the election...|["Gen. Zollicoffer t...|Ah, you've arrived j...|The election of Linc...|0.9210526315789473 |0.0               |0.9999999999666667                  |0.5                |
|What warnings were i...|["were not reported....|Well, friend, it see...|A warning letter rec...|0.9130434782608695 |0.0               |0.8666666666377778                  |1.0                |
|What role did the Bo...|["DELLEVILLEs ILL., ...|Well, it's good to s...|The Border State Com...|0.8125             |0.0               |0.8666666666377778                  |1.0                |
|What were the stock ...|['FnAEclAL---0n the ...|Ah, welcome to town!...|On the 10th, the sto...|1.0                |0.0               |0.8055555555287036                  |1.0                |
|What types of goods ...|['~\n\n\nHave now in...|Ah, welcome! You’ve ...|The context highligh...|0.4166666666666667 |0.8602855274745554|0.9166666666361111                  |0.6666666666666666 |
|What actions were ta...|['Tnk authorities Of...|Ah, welcome! You’ve ...|In Baltimore, suprem...|1.0                |0.0               |0.8055555555287036                  |0.16666666666666666|
|What were the public...|["sENArE.\nMI Thomps...|Ah, greetings! You’v...|The public meeting r...|0.64               |0.0               |0.99999999998                       |0.75               |
|What was the public ...|['An immense meeting...|Oh, I see you’re cur...|The public attendanc...|0.6666666666666666 |0.8948351213738149|0.9999999999                        |0.6666666666666666 |
|What was the nature ...|['CHARLESTON, Jan. 5...|Ah, welcome to our f...|The correspondence b...|0.9473684210526315 |0.0               |0.8041666666465626                  |1.0                |
|What was the signifi...|["orr BeSOUrCcS. - V...|Ah, welcome to our t...|The federal capital ...|0.8846153846153846 |0.0               |0.5888888888692593                  |0.5                |
|What were the sentim...|["That t d our arden...|Well, friend, you’ve...|The sentiments regar...|1.0                |0.0               |0.99999999998                       |1.0                |
|What were the postal...|["The Washington cor...|Well, let me tell yo...|The postal arrangeme...|0.6666666666666666 |0.0               |0.99999999998                       |1.0                |
|What was Kentucky's ...|["Louisville, April ...|Ah, welcome to Louis...|Kentucky's position ...|1.0                |0.0               |0.94999999997625                    |1.0                |
|What actions were ta...|["The Washington cor...|Ah, welcome to Richm...|During the State Con...|0.7307692307692307 |0.0               |0.8055555555287036                  |1.0                |
|What role did sugar ...|["gents r che SUGAR ...|Well, friend, sugar ...|The context mentions...|1.0                |0.0               |0.6791666666496875                  |0.6666666666666666 |
|What were the detail...|['~ id EIdl FE . "a ...|Well, I’m glad you'v...|In February 1851, th...|0.6842105263157895 |0.857546059961214 |0.99999999998                       |1.0                |
|Who were the key fig...|['The meeting was or...|I find it quite fasc...|The meeting was orga...|0.2777777777777778 |0.0               |0.0                                 |0.5                |
|What significant eve...|['didate in the Mays...|Ah, welcome to Maysv...|During the Civil War...|0.9285714285714286 |0.0               |0.0                                 |0.0                |
|What are the benefit...|['Greeleys Bourbon B...|Ah, welcome to our l...|Greeley's Bourbon Bi...|1.0                |0.0               |0.99999999998                       |0.75               |
|What are the benefit...|["u A single bottle ...|Well, let me tell yo...|A single bottle of S...|0.05555555555555555|0.0               |0.9999999999                        |0.5                |
|What happened to the...|['A patriotic New Yo...|Ah, you’ve arrived j...|The money sent by th...|0.36363636363636365|0.0               |0.9999999999                        |1.0                |
|What role did Camero...|['from exhaustion, b...|Ah, you’ve asked a g...|Cameron, likely refe...|0.35294117647058826|0.9491316994393055|0.7499999999625                     |0.5                |
|What types of goods ...|['Dealers in Dry Goo...|Ah, I see you’re cur...|The sale of grocerie...|0.4                |0.0               |0.9999999999666667                  |0.5                |
|How did the sentimen...|['ue said he appeare...|I tell you, the sent...|At the state convent...|1.0                |0.0               |0.99999999998                       |0.75               |
|What was the status ...|['WASHINGTON, Jan. 3...|Ah, my friend, you'v...|The status of the sl...|0.7142857142857143 |0.0               |0.9999999999666667                  |1.0                |
|What were the implic...|['BoaIuAs Jan ..\nGo...|Ah, welcome to town,...|The state tax increa...|0.04               |0.0               |0.94999999997625                    |1.0                |
|What significant eve...|["were not reported....|Ah, welcome! It’s go...|In September 1861, a...|0.7037037037037037 |0.0               |0.0                                 |0.0                |
|What orders were iss...|['May 18th 1S61.-Aud...|Well, friend, let me...|On May 10th, 1861, t...|0.45454545454545453|0.956056486663272 |0.9999999999666667                  |1.0                |
|What significant eve...|['CEALED PROPOs Al L...|Ah, you’ve arrived a...|In September 1861, a...|0.16666666666666666|0.0               |0.0                                 |0.0                |
|What was the signifi...|['May 18th 1S61.-Aud...|Well, let me tell yo...|The order issued by ...|0.16666666666666666|0.9431307491076341|0.8874999999778125                  |0.0                |
|What is the signific...|['TEE FIRs7 PosT OFF...|Ah, welcome to our f...|The significance of ...|0.17647058823529413|0.9546990444263512|0.8666666666377778                  |0.6666666666666666 |

</details>

✅ Averages:

- `faithfulness`: 0.639073783
- `answer_relevancy`: 0.2159191042
- `llm_context_precision_with_reference`: 0.7718409586
- `context_recall`: 0.6846405229

### ✅ Performance Analysis:

- Faithfulness (0.64): The pipeline shows moderate faithfulness, meaning generated answers are reasonably aligned with the retrieved context, though there's room for improvement in ensuring responses strictly adhere to source material.
- Answer Relevancy (0.22): This low score indicates a significant weakness - the system often generates answers that don't directly address the user's questions, suggesting the retrieval or answer generation components need refinement.
- Context Precision (0.77): The highest performing metric shows the system is good at retrieving relevant context when it has reference material, indicating the retrieval mechanism works well when proper references exist.
- Context Recall (0.68): Moderate performance suggests the system retrieves a reasonable portion of relevant information, but may miss some important context that could improve answer quality.

Overall Assessment: The system is good at finding relevant information but falls short when it comes to actually answering questions. The retrieval part works well - it can locate and extract the right context from the source material. However, the low answer relevancy score shows that the system often gives responses that don't really address what users are asking. This suggests the problem lies in how the system processes queries or generates answers, rather than in finding the right source material.

## Task 6: The Benefits of Advanced Retrieval

1. ✅ I intent to try a Multi-query retriever. Because the phrasing in historical docs can be quite different from modern language, rephrasing the query in several ways should help capture relevant docs.

2. ✅ I also plan to experiment with an ensemble retriever that combines the multi-query retriever with BM25. While BM25 alone may not be sufficient, integrating it with the multi-query approach could strike a good balance—retrieving semantically relevant documents while still capturing exact-match keywords like proper nouns, which may not be well-represented in embeddings.

## Task 7: Assessing Performance

| ✅ Metric                         | Baseline       | Multi-Query Retriever  | Ensemble Retriever  |
|-----------------------------------|----------------|------------------------|---------------------|
| Faithfulness                      | 0.639073783    | 0.6779925866           | 0.6682036381        |
| Answer Relevancy                  | 0.2159191042   | 0.2133997587           | 0.2130546932        |
| LLM Context Precision w/ Reference| 0.7718409586   | 0.7700213418           | 0.6706878846        |
| Context Recall                    | 0.6846405229   | 0.7254901961           | 0.7928571429        |

Looking at the performance metrics, the Ensemble Retriever performs best at Context Recall (0.793), meaning it finds the most relevant source information. The Multi-Query Retriever leads in Faithfulness (0.678), showing it generates responses that stick closest to the retrieved content. However, all three approaches score poorly on Answer Relevancy (around 0.21), indicating the generated answers don't actually answer the user's questions well. The Baseline does well on LLM Context Precision (0.772), suggesting it uses retrieved context effectively, but the Ensemble approach drops significantly here (0.671), possibly because combining multiple retrieval methods creates too much information to process efficiently. The results show that while advanced retrieval methods can improve finding relevant information, they still struggle with the core task of generating answers that directly address what users are asking.

My intuition is that we actually have a misalignment between how our synthetic data is generated and how we expect users to use an application. In other words, we aren't using the correct personas, and thus our testing isn't quite giving us the best picture of what's going on. Additionally, better prompting will certainly help.

### Expected Changes

1. ✅ This prototype is only embedding documents from one year, 1861. To be truly useful, I'll need to allow users to interact with a wide range of dates, either by selecting them explicitly or implying in their query.

2. ✅ Creating a more complex workflow using agentic reasoning could improve the user experience. For example, a user may ask a query that is general and spans many different times, like "How has the treatement of the flu evolved?" vs a single-time period question like "What did they know about germs in 1900?" Using an agentic query router could mean more intuitive responses that match what a given user is looking for.

3. ✅ Better evaluation of useful external APIs. It's not obvious to me that my external API is adding any value, especially compared to the extra latency. I would like to explore useful APIs, but they need to be solving a clear problem that currently isn't being addressed.

4. ✅ Make an interface that isn't horrible 😅