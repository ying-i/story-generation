## Web Application Architecture
<img src="https://github.com/ying-i/story-generation/blob/main/web%20application%20%20(4).jpg" width="700"/>
We first created our Gradio apps and hosted them on Hugging Face Spaces. Then, we queried the created Gradio apps within our Flask web application, which managed the backend operations including interaction with MongoDB database for data persistence.
The following are the gradio apps links:

- RAG-2 is using story.txt for RAG : https://huggingface.co/spaces/yiyii/RAG
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










