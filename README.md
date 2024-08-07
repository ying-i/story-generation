## Web Application Architecture
<img src="https://github.com/ying-i/story-generation/blob/main/web%20application%20%20(4).jpg" width="700"/>
We first create our gradio apps on Hugging Face Spaces, and then use the gradio_client Python library to query our gradio apps.
The following are the gradio apps links:

- RAG-2 is using story.txt for RAG : https://huggingface.co/spaces/yiyii/RAG-2
- RAG-3 is using uploaded PDFs for RAG: https://huggingface.co/spaces/yiyii/RAG-3



## Workflow of Story Generation
<img src="https://github.com/ying-i/story-generation/blob/main/workflow%20(4).jpg" width="500"/>
Techniques:

- using Deepface framework to get user's emotion, age, and gender
- using blip-image-caption-large model to get the image caption
- using RAG(Retrieval-Augmented Generation ) to get top-k most relevant story plots from story.txt or uploaded PDF files 
- using Mistral 7b model to generate a story












