## Web Application Architecture
<img src="https://github.com/ying-i/story-generation/blob/main/web%20application%20%20(4).jpg" width="700"/>
A web application that can generate a story based on uploaded face image. We first created our Gradio apps and hosted them on Hugging Face Spaces. Then, we queried the created Gradio apps within our Flask web application, which managed the backend operations including interaction with MongoDB database for data persistence.
The following are the gradio apps links:

- RAG is using story.txt for RAG : https://huggingface.co/spaces/yiyii/RAG
- RAG-3 is using uploaded PDFs for RAG: https://huggingface.co/spaces/yiyii/RAG-3



## Workflow of Story Generation
<img src="https://github.com/ying-i/story-generation/blob/main/workflow%20(4).jpg" width="500"/>
Techniques:

- using Deepface framework to get user's emotion, age, and gender
- using blip-image-caption-large model to get the image caption
- using RAG(Retrieval-Augmented Generation ) to get top-k most relevant story plots from story.txt or uploaded PDF files 
- using Mistral 7b model to generate a story

## Web Application Screenshots
<img src="https://github.com/ying-i/story-generation/blob/main/app-screenshot1.png" width="800"/>

<img src="https://github.com/ying-i/story-generation/blob/main/app-screenshot2.png" width="800"/>

<img src="https://github.com/ying-i/story-generation/blob/main/app-screenshot3.png" width="800"/>

<img src="https://github.com/ying-i/story-generation/blob/main/app-screenshot4.png" width="800"/>

## Abstract
Our work presents an approach to automated story generation by integrating facial expression analysis and retrieval of existing stories with
a Large Language Model. The system utilizes the DeepFace framework to analyze facial attributes such as emotion, age, gender from an
input face image, and also it uses BLIP model to generate an image caption. These elements, combined with retrieved plots from an external knowledge base using Retrieval Augmented Generation (RAG), are then fed into the Mistral 7B language model to generate a story. Our results show that including the emotion factor leads to more emotion-related words in generated stories. However, incorporating the emotion factor in story generation is not always beneficial to all metrics (Fluency, Coherency, Relevance, Emotional Resonance, and Likability). Similarly, inclusion of retrieved plots helps to increase the length of generated stories, but this does not always positively impact all metrics (Fluency, Coherency, Relevance, Plot Appeal, and Likability).






