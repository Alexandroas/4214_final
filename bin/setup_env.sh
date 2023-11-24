python -m venv venv
activate () {
    .venv/Scripts/activate
    echo "installing requirement to virtual enviroment"
    pip install -r requiremtns.txt
}
activate