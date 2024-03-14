from sqlalchemy import create_engine, text

# from env import username, password, db_name, host, port

engine = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engine.connect()
connections.close()
