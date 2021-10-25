# Importação das bibliotecas
import requests as req
import pandas as pd

# Função para buscar os indices
def consulta_api_indice(indice):
    '''
        ## Retorna JSON da série histórica da inflação.
        
        ### Parâmetros:
            indice (str): Indice a ser buscado ('IGPM' ou 'IPCA')   
            
        ---------------------------------------------------------------------------------
        
        Fonte: http://www.ipeadata.gov.br/
            
            IPCA: 
            Preços: Índice de Preços ao Consumidor Amplo (IPCA) geral com índice base (dez. 1993 = 100)
            Frequência: Mensal de 1979.12 até 2021.01
            Fonte: Instituto Brasileiro de Geografia e Estatística, Sistema Nacional de Índices de Preços ao Consumidor (IBGE/SNIPC)
           
            IGPM:
            Preços: índice geral de preços do mercado (IGP-M) - geral: índice (ago. 1994 = 100)
            Frequência: Mensal de 1989.06 até 2021.02
            Fonte: Fundação Getulio Vargas, Conjuntura Econômica - IGP (FGV/Conj. Econ. - IGP)
            
    '''
    def __filter__(item):
        """
        Filtra dados a partir do valor de referencia (Fator Acumulado = 100)
        """
        if item["fatorAcumulado"] >= 100:
            return True
        return False
        
    
    
    if indice.upper() not in ["IPCA","IGPM"]:
        raise Exception("Parametro inválido. Esperava-se 'IPCA' ou 'IGPM', recebeu {}".format(indice.upper()))
        return
    
    BASE_URL = "http://www.ipeadata.gov.br/api/odata4//ValoresSerie(SERCODIGO='{}')"
    SERCODIGO= {
        "IPCA":"PRECOS12_IPCA12",
        "IGPM":"IGP12_IGPM12"
    }
    
    
    response = req.get(BASE_URL.format(SERCODIGO[indice.upper()]))
    if response.status_code != 200:
        raise Exception("Algo deu errado")
    else:
        data = response.json()["value"]
        df = pd.DataFrame(data=filter(__filter__,[{"data":x["VALDATA"].split("T")[0],"fatorAcumulado":x["VALVALOR"]} for x in data]))
        df["tipoIndice"] = indice
        return df

# Inclusão colunas extra (indice mensal, cenario, fator acumulado positivo)
def get_api_indice():    
    series = [consulta_api_indice("IPCA"), consulta_api_indice("IGPM")]
    for serie in series:
        serie['data'] = serie['data'].astype('datetime64[ns]')
        #serie.sort_values(by=["data"], inplace=True)
        var_mes_list = []
        acum_positivo = []
        for idx in serie.index:
            try:
                var = serie["fatorAcumulado"][idx]/serie["fatorAcumulado"][idx-1] - 1 
            except:
                var = 0
            var_mes_list.append(var *100)
            #var_mes_list.append(round(var *100,4))
            #print('idx)
            if var>=0:
                var_pos = var + 1
            else:
                var_pos = 1

            try:
                acum = acum_positivo[idx - 1]*var_pos
            except:
                acum = 100
            acum_positivo.append(acum)

        serie["indiceMensal"]= var_mes_list 
        serie["fatorAcumuladoPositivo"] = acum_positivo
        serie["cenario"] = "Oficial"

        df = pd.concat(series)
        df = df.infer_objects()
        
        def indiceMensalPositivo(df):
            i = df['indiceMensal']
            if (i <= 0):
                texto = 0
                return texto
            else:
                texto = i
                return texto
        df['indiceMensalPositivo'] = df.apply(indiceMensalPositivo, axis = 1)
    return df

# Função para retornar o DataFrame
def run():
    dff = get_api_indice()
    print(">> Concluído")
    return dff

if __name__ == "__main__":
    dff = run()
    print(dff)
