from amadeus import Flights
import csv
import time

flights = Flights('<YOUR API KEY HERE>')

with open('prices.csv', 'a+') as csvprecos:
    fieldnames = ['DataPesquisa','Origem', 'Destino', 'DataIda', 'Preco']

    writer = csv.DictWriter(csvprecos, fieldnames=fieldnames)

    writer.writeheader()

with open('viagens.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in csvreader:

        datapesquisa = time.strftime("%d-%m-%Y")
        origem = row[0]
        destino = row[1]
        dataida = row[2]

        result = flights.low_fare_search(
            origin=origem,
            destination=destino,
            currency='BRL',
            departure_date=dataida,
            )

        data = result

        if ('status' in result and result['status']== 400):
            with open('prices.csv', 'a+') as csvprecos:
                writer = csv.DictWriter(csvprecos, fieldnames=fieldnames)
                writer.writerow({'DataPesquisa': datapesquisa, 'Origem': origem, 'Destino': destino, 'DataIda': dataida,
                                  "Preco": "NAO ENCONTRADA"})

        else:
            try:
                preco = data['results'][0]['fare']['total_price']

            except:
                print ("Erro na consulta. Timeout de 1 minuto antes de tentar novamente")
                preco = "ERRO - TENTAR NOVAMENTE"
                time.sleep(60)
                print ("Timeout Finalizado")
            with open('prices.csv', 'a+') as csvprecos:
                writer = csv.DictWriter(csvprecos, fieldnames=fieldnames)
                writer.writerow({'DataPesquisa': datapesquisa, 'Origem': origem, 'Destino': destino, 'DataIda': dataida,
                                  "Preco": preco})
