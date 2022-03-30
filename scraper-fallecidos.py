import pandas as pd
import requests
from io import StringIO


def summary_by_department(df):

  df=df[['FECHA_FALLECIMIENTO','SEXO', 'EDAD_DECLARADA']].groupby(['FECHA_FALLECIMIENTO', 'SEXO']).count()
  df=df.reset_index()
  df=df.pivot(index='FECHA_FALLECIMIENTO', columns='SEXO', values='EDAD_DECLARADA')
  df=df.rename_axis(None, axis=1)
  df=df.fillna(0).astype('int')

  return df

try:
  url = "https://cloud.minsa.gob.pe/s/xJ2LQ3QyRW38Pe5/download"
  headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
  req = requests.get(url, headers=headers)
  data = StringIO(req.text)

  df=pd.read_csv(data, sep=';', usecols=['FECHA_CORTE', 'EDAD_DECLARADA', 'SEXO', 'FECHA_FALLECIMIENTO', 'DEPARTAMENTO'], parse_dates=['FECHA_FALLECIMIENTO'])
  #df=pd.read_csv('fallecidos_covid.csv', sep=';', usecols=['FECHA_CORTE', 'EDAD_DECLARADA', 'SEXO', 'FECHA_FALLECIMIENTO', 'DEPARTAMENTO'], parse_dates=['FECHA_FALLECIMIENTO'])
  df=df[(df['SEXO']=='FEMENINO') | (df['SEXO']=='MASCULINO')]
  fecha_corte=df['FECHA_CORTE'].drop_duplicates().set_axis(['fecha_corte'])
  fecha_corte.to_json("resultados/fecha_corte_fallecidos.json")

  # DIARIO FALLECIDOS
  df_fallecidos=df[['FECHA_FALLECIMIENTO','SEXO', 'EDAD_DECLARADA']].groupby(['FECHA_FALLECIMIENTO', 'SEXO']).count()
  df_fallecidos=df_fallecidos.reset_index()
  df_fallecidos=df_fallecidos.pivot(index='FECHA_FALLECIMIENTO', columns='SEXO', values='EDAD_DECLARADA')
  df_fallecidos=df_fallecidos.rename_axis(None, axis=1)
  df_fallecidos=df_fallecidos.fillna(0).astype('int')
  df_fallecidos

  # ACUMULADO FALLECIDOS
  df_fallecidos_cum=df_fallecidos.cumsum()
  df_fallecidos_cum

  col_poblacion=[452125,
  1189403,
  440629,
  1488247,
  658081,
  1528904,
  1090990,
  1392648,
  414882,
  823560,
  889916,
  1340064,
  1955991,
  1325269,
  10741923,
  1096407,
  170503,
  190442,
  283946,
  1966703,
  1221523,
  920842,
  365771,
  235194,
  597287]

  # ACUMULADO POR DEPARTAMENTO
  df_fallecidos_departamento=df[['DEPARTAMENTO','SEXO']]
  def function(valueX):
    if 'LIMA' in valueX:
      return 'LIMA'
    else:
      return valueX
  df_fallecidos_departamento['DEPARTAMENTO']=df_fallecidos_departamento['DEPARTAMENTO'].map(function)
  df_fallecidos_departamento=df_fallecidos_departamento.groupby(['DEPARTAMENTO']).count()
  df_fallecidos_departamento['POBLACION']=col_poblacion
  df_fallecidos_departamento['INDICE']=round(df_fallecidos_departamento['SEXO']/(df_fallecidos_departamento['POBLACION']/100000)).astype('int')
  df_fallecidos_departamento

  # ACUMULADO POR GRUPO ETARIO
  bins = [18,20,30,40,50,60,70,80,df['EDAD_DECLARADA'].max()+1]
  labels = ['18 a 19 años','20 a 29 años','30 a 39 años','40 a 49 años','50 a 59 años','60 a 69 años','70 a 79 años','80 años a más']
  poblacion_por_grupo_etario = [900000,5700000,5300000,4400000,3300000,2300000,1300000,700000] 
  df_fallecidos_edades = df
  df_fallecidos_edades['GRUPO_ETARIO'] = pd.cut(df['EDAD_DECLARADA'], bins=bins, labels=labels, right=False)
  df_fallecidos_edades = df_fallecidos_edades.groupby(['GRUPO_ETARIO'])["SEXO"].count().reset_index()
  df_fallecidos_edades.rename(columns = {'SEXO':'FALLECIDOS'}, inplace = True)
  df_fallecidos_edades['POBLACION']=poblacion_por_grupo_etario
  df_fallecidos_edades['PORCENTAJE']=round(df_fallecidos_edades['FALLECIDOS']/df_fallecidos_edades['POBLACION']*100,2)
  df_fallecidos_edades=df_fallecidos_edades.set_index('GRUPO_ETARIO')
  df_fallecidos_edades

  #TOTAL FALLECIDOS
  #fallecidos = pd.Series([df['FECHA_CORTE'].unique()[0], df[['FECHA_CORTE'][0]].count(), df_fallecidos.tail(1).sum(axis=1)[0]], index=['fecha_corte', 'total_fallecidos', 'incremento_fallecidos'])
  #fallecidos.to_json('resultados/fallecidos.json')

  # DIARIO POR DEPARTAMENTO
  list_departamentos = ["AMAZONAS",
                    "ANCASH",
                    "APURIMAC",
                    "AREQUIPA",
                    "AYACUCHO",
                    "CAJAMARCA",
                    "CALLAO",
                    "CUSCO",
                    "HUANCAVELICA",
                    "HUANUCO",
                    "ICA",
                    "JUNIN",
                    "LA LIBERTAD",
                    "LAMBAYEQUE",
                    "LIMA",
                    "LORETO",
                    "MADRE DE DIOS",
                    "MOQUEGUA",
                    "PASCO",
                    "PIURA",
                    "PUNO",
                    "SAN MARTIN",
                    "TACNA",
                    "TUMBES",
                    "UCAYALI"]

  for department_name in list_departamentos:
      df_by_department=df[df['DEPARTAMENTO'] == department_name]
      df_filtered=summary_by_department(df_by_department)
      df_filtered.to_csv(f"resultados/fallecidos_departamentos/{department_name.lower()}.csv")


  df_fallecidos.to_csv('resultados/fallecidos_diarios.csv')
  df_fallecidos_cum.to_csv('resultados/fallecidos_acumulados.csv')
  df_fallecidos_departamento.to_csv('resultados/fallecidos_por_departamentos.csv')
  df_fallecidos_edades.to_csv('resultados/fallecidos_por_edades.csv')

except ConnectionResetError:
  pass