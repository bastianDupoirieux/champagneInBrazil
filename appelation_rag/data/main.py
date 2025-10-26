import data_gatherer
import yaml
import pdf_reader
import time

#Define run options here
beverage_type = 'Vin'
region = 'Alsace et Est'

with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)


def main(beverage_type, region, max_tries = 5):


    appellations = pdf_reader.read_pdf_table(config['appellation_list_file'])
    appellations = appellations[appellations['Type de produits 1'] == beverage_type]
    appellations = appellations[appellations['Bassin']==region]

    appellations_list = list(appellations['Nom de l\'appellation'])
    #appellations_list = ['Alsace']
    i = 1
    while i <= max_tries and len(appellations_list) > 0:
        print(f'---------------TRY {i}/{max_tries}, fetching results for {len(appellations_list)} appellations----------------------')
        driver = data_gatherer.setup_driver_options(config['driver'], config['appellations_definition_dir'])
        search = data_gatherer.get_multiple_search_results(driver, appellations_list)
        i += 1
        print(search)
        appellations_list = search["error"]
        time.sleep(10)



if __name__=='__main__':
    main(beverage_type, region)