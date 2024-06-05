import dash

from config import exibir_dashboard


def main():

    app = dash.Dash(__name__)
        
    exibir_dashboard(app)
    
    app.run_server(debug=True)

if __name__ == '__main__':
    main()
