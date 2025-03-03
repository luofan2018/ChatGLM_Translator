import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import ChatGLMModel, OpenAIModel
from translator import PDFTranslator
#import webbrowser
import gradio  as gr
#import markdown

def processData(pdf_file_path,file_format):
    translator = PDFTranslator(model)
    output_file_path=translator.translate_pdf(pdf_file_path, file_format)
    with open(output_file_path,encoding="utf8") as f:
        output=f.read()
    return(output)


if __name__ == "__main__":

    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    #model = OpenAIModel(model=model_name, api_key=api_key)
    from transformers import AutoTokenizer, AutoModel
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True, device='cuda')
    model = model.eval()
    model = ChatGLMModel(model=model,tokenizer=tokenizer,history=[])
    
    iface = gr.Interface(
        fn=processData,
        inputs=[
            gr.Textbox(label="请提供pdf地址(无引号)："),
            gr.Radio(label="翻译完成 存储文件类型",choices=["pdf","markdown"],value="markdown"),
        ],
        outputs=[
            gr.Text(label="翻译结果"),
        ],
        title="pdf AI机翻",
        description="gpt机翻pdf，无图纯文字",
    )
    
    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    # translator = PDFTranslator(model)
    # translator.translate_pdf(pdf_file_path, file_format)
    iface.launch(
        #server_name=SERVER_NAME,server_port=SERVER_PORT
        )
    iface.close()