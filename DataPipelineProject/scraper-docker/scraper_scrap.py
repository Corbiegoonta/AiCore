
def upload_dataframe_to_rds1(self, host = 'lolchampiondatabase.cudnxxlhkqef.eu-west-2.rds.amazonaws.com',
    port = int(3306),
    user = 'corbie',
    password = 'leagueoflegends',
    database = 'lolchampiondatabase'):
    
    try:
        champion_dataframe = self.create_dataframe()
        print(f'Dataframe {champion_dataframe} was created succefully.')
    except Exception as e:
        print('Creation of dataframe was unsuccessful.')
        print(e)
    
    conn = pymysql.connect(host=host, user=user, passwd=password, connect_timeout=10)
    with conn.cursor() as cur:
        cur.execute('create database bsb-round;')
        
    try:
        championdatadb = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + database , echo=False)
        print('Create_engine successful.')
        champion_dataframe.to_sql(name='finalchampdb', con=championdatadb, if_exists='replace', index=False)
        print('To_sql successful.')
    except Exception as e:
        print(e)
    pass


def upload_dataframe_to_rds2(host = 'lolchampiondatabase.cudnxxlhkqef.eu-west-2.rds.amazonaws.com',
    port = str(3306),
    user = 'corbie',
    password = 'leagueoflegends',
    rds_database = 'lolchampiondatabase',
    sql_database = 'tabl'):
    
    alcheng = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + port + '/' + sql_database , echo=False)
    
    connection = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            db=sql_database)

    cursor = connection.cursor()
    
    try:
        dblist = cursor.execute('SHOW DATABASES')
        print('Sql shown successfully.1')
    except Exception as e:
        print('Sql database was not shown.1')

    try:
        cursor.execute(f'CREATE DATABASE {sql_database}')
        print('Sql database created successfully.')
    except Exception as e:
        print(e)
        print('Sql database was not created.')

    try:
        cursor.execute('SHOW TABLES')
        print('Sql shown tables successfully.2')
    except Exception as e:
        print(e)
        print('Sql tables were not shown.2')

    for i in cursor:
        print(i)

    try:
        test_dict = {'apple' : [1]}
        test_df = pd.DataFrame(test_dict)
        print('Dataframe was created succefully.')
    except Exception as e:
        print('Creation of dataframe was unsuccessful.')
        print(e)
    
    try:
        test_df.to_sql(name='Champion_Data_Table', con=alcheng, if_exists='replace', index=False)
        print('To_sql successful.')
    except Exception as e:
        print(e)
    pass

    cursor.execute('SELECT * FROM Champion_Data_Table')

    cursor.fetchall()

    for i in cursor:
        print(i)
    
    connection.close()