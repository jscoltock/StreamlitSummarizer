from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks import get_openai_callback 
from langchain.prompts import PromptTemplate


from dotenv import load_dotenv

load_dotenv()

def initialize_llm(model, openai_api_key):
    if model == "gpt 3.5 turbo (cheap)":
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0,openai_api_key=openai_api_key)
    else:
        return ChatOpenAI(model="text-davinci-003", temperature=0,openai_api_key=openai_api_key)

def split_text(essay, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.create_documents([essay])

def load_summary_chain( llm, basic_prompt, refine_prompt):

    prompt_template = basic_prompt + """
    {text}
    SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    refine_template = (
        "Your job is to produce a final summary\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"

        "Return the original summary."
        "Given the new context, " + refine_prompt +
        "If the context isn't useful, return the original summary."
    )

    refine_prompt = PromptTemplate.from_template(refine_template)

    return load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_text"
    )

def run_logic(model, uploaded_file, input_text, chunk_size, chunk_overlap, basic_prompt, refine_prompt, openai_api_key):
    essay = uploaded_file.read().decode() if uploaded_file else input_text  
    llm = initialize_llm(model, openai_api_key)
    docs = split_text(essay, chunk_size, chunk_overlap)

    summary_chain = load_summary_chain(llm, basic_prompt, refine_prompt)

    with get_openai_callback() as cb:
        result = summary_chain({"input_documents": docs}, return_only_outputs=False)
    
    return "Method: refine" + " LLM: " + model + " Total cost: $" + str(cb.total_cost) + ". \n\n " + result["output_text"]
