import pandas as pd
import requests
from io import StringIO

def summary_by_department(df):

  df=df[['FECHA_RESULTADO','METODODX','SEXO']].groupby(['FECHA_RESULTADO','METODODX']).count()
  df=df.reset_index()
  df=df.pivot(index='FECHA_RESULTADO', columns='METODODX', values='SEXO')
  df=df.rename_axis(None, axis=1)
  df=df.fillna(0).astype('int')

  return df



try:
  url = "https://files.minsa.gob.pe/s/eRqxR35ZCxrzNgr/download"
  headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
  req = requests.get(url, headers=headers)
  data = StringIO(req.text)

  df=pd.read_csv(data, sep=';', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_RESULTADO', 'METODODX', 'DEPARTAMENTO'], parse_dates=['FECHA_RESULTADO'], dtype={'FECHA_CORTE': str})
  #df=pd.read_csv('positivos_covid.csv', sep=';', usecols=['FECHA_CORTE', 'EDAD', 'SEXO', 'FECHA_RESULTADO', 'METODODX', 'DEPARTAMENTO'], parse_dates=['FECHA_RESULTADO'])
  fecha_corte=df['FECHA_CORTE'].bfill().ffill().drop_duplicates().set_axis(['fecha_corte'])
  fecha_corte.to_json("resultados/fecha_corte_positivos.json")

  # DIARIO AG, PCR, PR
  df_positivos=df[['FECHA_RESULTADO','METODODX','SEXO']].groupby(['FECHA_RESULTADO','METODODX']).count()
  df_positivos=df_positivos.reset_index()
  df_positivos=df_positivos.pivot(index='FECHA_RESULTADO', columns='METODODX', values='SEXO')
  df_positivos=df_positivos.rename_axis(None, axis=1)
  df_positivos=df_positivos.fillna(0).astype('int')
  df_positivos

  # ACUMULADO AG, PCR, PR
  df_positivos_cum=df_positivos.cumsum()
  df_positivos_cum

  # DIARIO AG, PCR, PR DESDE 2022
  df_positivos_2022=df_positivos[df_positivos.index >= '2022-01-01']
  df_positivos_2022

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
  df_positivos_departamento=df[['DEPARTAMENTO','METODODX']].dropna()
  def function(valueX):
    if 'LIMA REGION' in valueX:
      return 'LIMA'
    elif 'ARICA' in valueX:
      return 'TACNA'
    elif 'CARACAS' in valueX:
      return 'TUMBES'
    else:
      return valueX
  df_positivos_departamento['DEPARTAMENTO']=df_positivos_departamento['DEPARTAMENTO'].map(function)
  df_positivos_departamento=df_positivos_departamento.groupby(['DEPARTAMENTO']).count()
  df_positivos_departamento['POBLACION']=col_poblacion
  df_positivos_departamento['INDICE']=round(df_positivos_departamento['METODODX']/(df_positivos_departamento['POBLACION']/100000)).astype('int')
  df_positivos_departamento

  # ACUMULADO POR GRUPO ETARIO
  bins = [18,20,30,40,50,60,70,80,df['EDAD'].max()+1]
  labels = ['18 a 19 años','20 a 29 años','30 a 39 años','40 a 49 años','50 a 59 años','60 a 69 años','70 a 79 años','80 años a más']
  poblacion_por_grupo_etario = [900000,5700000,5300000,4400000,3300000,2300000,1300000,700000] 
  df_positivos_edades = df
  df_positivos_edades['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
  df_positivos_edades = df_positivos_edades.groupby(['GRUPO_ETARIO'])["METODODX"].count().reset_index()
  df_positivos_edades.rename(columns = {'METODODX':'POSITIVOS'}, inplace = True)
  df_positivos_edades['POBLACION']=poblacion_por_grupo_etario
  df_positivos_edades['PORCENTAJE']=round(df_positivos_edades['POSITIVOS']/df_positivos_edades['POBLACION']*100,2)
  df_positivos_edades=df_positivos_edades.set_index('GRUPO_ETARIO')
  df_positivos_edades

  # ACUMULADO POR GRUPO ETARIO - 2022
  bins = [5,12,18,30,40,50,60,80,df['EDAD'].max()+1]
  labels = ['5 a 11 años','12 a 17 años','18 a 29 años','30 a 39 años','40 a 49 años','50 a 59 años','60 a 79 años','80 años a más']
  poblacion_por_grupo_etario = [4201842,3614488,6788969,5382481,4604711,3524112,3851743,812904]
  df_positivos_edades_2022 = df[df['FECHA_RESULTADO']>= '2022-06-26']
  df_positivos_edades_2022['GRUPO_ETARIO'] = pd.cut(df['EDAD'], bins=bins, labels=labels, right=False)
  df_positivos_edades_2022 = df_positivos_edades_2022.groupby(['GRUPO_ETARIO'])["METODODX"].count().reset_index()
  df_positivos_edades_2022.rename(columns = {'METODODX':'POSITIVOS'}, inplace = True)
  df_positivos_edades_2022['POBLACION']=poblacion_por_grupo_etario
  df_positivos_edades_2022['PORCENTAJE']=round(df_positivos_edades_2022['POSITIVOS']/df_positivos_edades_2022['POBLACION']*100,2)
  df_positivos_edades_2022=df_positivos_edades_2022.set_index('GRUPO_ETARIO')
  df_positivos_edades_2022

  #TOTAL POSITIVOS
  #positivos = pd.Series([df['FECHA_CORTE'].unique()[0], df[['FECHA_CORTE'][0]].count(), df_positivos.tail(1).sum(axis=1)[0]], index=['fecha_corte', 'total_positivos', 'incremento_positivos'])
  #positivos.to_json('resultados/positivos.json')

  from requests_html import HTMLSession
  session = HTMLSession()
  r = session.get('https://www.gob.pe/coronavirus#casos')
  scrap_covid_acumulado = r.html.find('.text-base.w-full.tracking-tight')
  scrap_covid_diario = r.html.find('.font-bold.text-2xl')
  scrap_covid = scrap_covid_acumulado + scrap_covid_diario
  d = []
  for number in scrap_covid:
      d.append(number.text)
  covid = pd.Series(d,index=['total_confirmados', 'total_altas', 'total_fallecidos', 'ayer_confirmados', 'ayer_altas', 'ayer_fallecidos'])
  covid.to_json('resultados/covid.json')


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
      df_filtered.to_csv(f"resultados/positivos_departamentos/{department_name.lower()}.csv")

  df_positivos.to_csv('resultados/positivos_diarios.csv')
  df_positivos_cum.to_csv('resultados/positivos_acumulados.csv')
  df_positivos_departamento.to_csv('resultados/positivos_por_departamentos.csv')
  df_positivos_edades.to_csv('resultados/positivos_por_edades.csv')
  df_positivos_2022.to_csv('resultados/positivos_diarios_2022.csv')
  df_positivos_edades_2022.to_csv('resultados/positivos_por_edades_2022.csv')

except ConnectionResetError:
  # error de peers
  pass