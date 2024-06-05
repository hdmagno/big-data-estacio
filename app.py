import dash

from config import preparar_dados, exibir_dados


def main():

    app = dash.Dash(__name__)
    
    x = input("Preparar dados? [s/n] ")
    
    if x == "s":
        preparar_dados()
        
    exibir_dados(app)
    
    app.run_server(debug=True)

if __name__ == '__main__':
    main()
