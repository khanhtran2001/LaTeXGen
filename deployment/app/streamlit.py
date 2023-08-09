import requests
from PIL import Image
import streamlit

if __name__ == "__main__":
    streamlit.set_page_config(page_title='LaTeXGen')
    streamlit.title('LaTeXGen')
    streamlit.markdown('Convert images of equations to corresponding LaTeX code.\n')

    uploaded_file = streamlit.file_uploader(
        'Upload an image an equation',
        type=['png', 'jpg'],
    )

    sampling_type_list = ["Nucleus","Random"]
    #sampling_type = streamlit.selectbox(label="Sampling type", options=sampling_type_list)

    default_temperature = 0.22
    temperature = streamlit.slider(label="Temperature", min_value=0.0, max_value=1.0, value=default_temperature)

    search_option_list = ["Greedy", "Beam"]
    search_option = streamlit.selectbox(label="Searching algorithm",options=search_option_list)

    beam_width_disable = True
    default_beam_width_depth = 3
    if search_option ==  "Beam":
        beam_width_disable = False
    beam_width_depth = streamlit.number_input(label="Beam width depth", min_value=1, max_value=10, value=default_beam_width_depth, disabled=beam_width_disable)

    config_data =  {
        #"sampling_type": sampling_type.lower(),
        "temperature": temperature,
        "search_type": search_option.lower(),
        "beam_width": beam_width_depth
    }

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        streamlit.image(image)
    else:
        streamlit.text('\n')
    

    if streamlit.button('Convert'):
        if uploaded_file is not None and image is not None:
            with streamlit.spinner('Computing'):
                response = requests.post('http://127.0.0.1:8000/predict/', files = {"file" : uploaded_file.getvalue()}, data = config_data)
            if response.ok:
                latex_code_list = response.json()
                if search_option == "Greedy":
                    latex_code = latex_code_list[0][0][0]
                    streamlit.code(latex_code, language='latex')
                    streamlit.markdown(f'$\\displaystyle {latex_code}$')
                else:
                    for i in range(beam_width_depth):
                        col1, col2 = streamlit.columns([0.9,0.1])
                        with col1:
                            latex_code = latex_code_list[0][i][0]
                            streamlit.code(latex_code, language='latex')
                            streamlit.markdown(f'$\\displaystyle {latex_code}$')
                        with col2:
                            percentage = latex_code_list[0][i][1]
                            percentage = f'{percentage:.3f}'
                            streamlit.markdown(percentage)
            else:
                streamlit.error(response.text)
        else:
            streamlit.error('Please upload an image.')