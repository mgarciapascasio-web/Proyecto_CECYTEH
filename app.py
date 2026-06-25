def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
    
    # Esta es la forma más directa de conectar usando el ID de tu URL
    # Tu ID es: 1HS8LB5Y79KXvgaco_Ry420thbPNRKpOQObC6AhREMJQ
    sh = gc.open_by_key("1HS8LB5Y79KXvgaco_Ry420thbPNRKpOQObC6AhREMJQ")
    
    # Esto obtiene la primera pestaña, sin importar su nombre
    return sh.get_worksheet(0)
