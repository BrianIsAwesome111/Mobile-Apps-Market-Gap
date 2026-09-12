mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"brianxiong1998@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
base=\"light\"\n\
primaryColor=\"white\"\n\
" > ~/.streamlit/config.toml
