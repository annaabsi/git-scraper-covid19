import pandas as pd
import py7zr
import requests
from py_essentials import hashing as hs

try:
    url = "https://cloud.minsa.gob.pe/s/Q6S9qAwfwE6c49X/download"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    req = requests.get(url, headers=headers)

    with open('TB_F100_SICOVID.7z', 'wb') as f:
        f.write(req.content)

    hash_downloaded = hs.fileChecksum("TB_F100_SICOVID.7z", "sha256")

    # Get hash saved
    with open('resultados/hash_scraper_pruebas.txt') as f:
        hash_saved = f.readlines()[0]

    if hash_saved==hash_downloaded:
        print("SAME FILE")
    else:
        print("DIFFERENT FILE")

        with py7zr.SevenZipFile('TB_F100_SICOVID.7z', mode='r') as z:
            z.extractall()

        df=pd.read_csv('TB_F100_SICOVID.csv', parse_dates=['fecha_prueba'], infer_datetime_format=True, converters = {'id_ubigeo_prueba': str})

        # DATA UBIGEOS
        df_id_ubigeo = pd.read_csv('TB_UBIGEOS.csv', converters = {'id_ubigeo': str, 'ubigeo_inei': str})
        df_id_ubigeo

        # TIPOS DE PRUEBAS POR DIA
        df_pruebas=df[['fecha_prueba','id_tipo_prueba','id_persona']].groupby(['fecha_prueba','id_tipo_prueba']).count()
        df_pruebas=df_pruebas.reset_index()
        df_pruebas=df_pruebas.pivot(index='fecha_prueba', columns='id_tipo_prueba', values='id_persona')
        df_pruebas=df_pruebas.rename_axis(None, axis=1)
        df_pruebas.columns=['Serológica','Antígena','Quimioluminiscencia']
        df_pruebas=df_pruebas.fillna(0).astype('int')
        df_pruebas

        # TIPOS DE PRUEBAS ACUMULADO
        df_pruebas_cum=df_pruebas.cumsum()
        df_pruebas_cum

        # PRUEBAS RÁPIDAS RESULTADOS POR DIA
        df_serologicas=df[df['id_tipo_prueba']==1].groupby(['fecha_prueba','id_resultado_prueba']).count()
        df_serologicas=df_serologicas.reset_index()
        df_serologicas=df_serologicas.pivot(index='fecha_prueba', columns='id_resultado_prueba', values='id_persona')
        df_serologicas=df_serologicas.rename_axis(None, axis=1)
        df_serologicas.columns=['Negativo','IgG Positivo','IgM e IgG Positivo','IgM Positivo']
        df_serologicas=df_serologicas.fillna(0).astype('int')
        df_serologicas

        # PRUEBAS RÁPIDAS RESULTADOS ACUMULADO
        df_serologicas_cum=df_serologicas.cumsum()
        df_serologicas_cum

        # PRUEBAS ANTIGENO RESULTADOS POR DIA
        df_antigeno=df[df['id_tipo_prueba']==2].groupby(['fecha_prueba','id_resultado_prueba']).count()
        df_antigeno=df_antigeno.reset_index()
        df_antigeno=df_antigeno.pivot(index='fecha_prueba', columns='id_resultado_prueba', values='id_persona')
        df_antigeno=df_antigeno.rename_axis(None, axis=1)
        df_antigeno.columns=['Negativo','Positivo','IgM e IgG Positivo']
        df_antigeno=df_antigeno.fillna(0).astype('int')
        df_antigeno

        # PRUEBAS ANTIGENO RESULTADOS ACUMULADO
        df_antigeno_cum=df_antigeno.cumsum()
        df_antigeno_cum

        # TIPOS DE PRUEBAS POR DISTRITO
        df_ubigeo=df[['id_ubigeo_prueba','id_tipo_prueba','id_persona']].groupby(['id_ubigeo_prueba','id_tipo_prueba']).count()
        df_ubigeo=df_ubigeo.reset_index()
        df_ubigeo=df_ubigeo.pivot(index='id_ubigeo_prueba', columns='id_tipo_prueba', values='id_persona')
        df_ubigeo=df_ubigeo.rename_axis(None, axis=1)
        df_ubigeo.columns=['Serológica','Antígena','Quimioluminiscencia']
        df_ubigeo=df_ubigeo.fillna(0).astype('int')

        # EQUIVALENTES DE ID UBIGEO
        df_ubigeo = pd.merge(df_ubigeo, df_id_ubigeo[['id_ubigeo','ubigeo_inei','departamento', 'provincia', 'distrito']],  how='inner', left_on='id_ubigeo_prueba', right_on='id_ubigeo')
        df_ubigeo

        # TIPOS DE PRUEBAS POR PROVINCIA
        df_provincia = df_ubigeo[['Serológica','Antígena','Quimioluminiscencia','provincia']].groupby(['provincia']).sum()
        df_provincia

        # TIPOS DE PRUEBAS POR DEPARTAMENTO
        df_departamento = df_ubigeo[['Serológica','Antígena','Quimioluminiscencia','departamento']].groupby(['departamento']).sum()
        df_departamento

        df_pruebas.to_csv('resultados/pruebas.csv')
        df_pruebas_cum.to_csv('resultados/pruebas_acumulado.csv')
        df_serologicas.to_csv('resultados/pruebas_serologicas.csv')
        df_serologicas_cum.to_csv('resultados/pruebas_serologicas_acumulado.csv')
        df_antigeno.to_csv('resultados/pruebas_antigeno.csv')
        df_antigeno_cum.to_csv('resultados/pruebas_antigeno_acumulado.csv')
        df_ubigeo.to_csv('resultados/pruebas_por_distrito.csv')
        df_provincia.to_csv('resultados/pruebas_por_provincia.csv')
        df_departamento.to_csv('resultados/pruebas_por_departamento.csv')

        # Save new hash
        file = open('resultados/hash_scraper_pruebas.txt', 'w')
        file.write(hash_downloaded)
        file.close()

except ConnectionResetError:
    # error de peers
    pass
