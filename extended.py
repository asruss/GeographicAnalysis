from estaty.analysis.action import Analyzer
from estaty.data_source.action import DataSource
from estaty.main import EstateModel
from estaty.merge.action import Merger
from estaty.preprocessing.action import Preprocessor
from estaty.report.action import Report


import warnings
warnings.filterwarnings('ignore')



def launch_parks_with_quercus_proximity_analysis():
   
   point_for_analysis = {'lat': 59.944843895537566, 'lon': 30.294778398601856}

   #1 Этап – определяем источники данных и получаем из них данные
   osm_source = DataSource('osm', params={'category': 'park'})
   bio_source = DataSource('csv', params={'path': './data/quercus_spb.csv',
                                          'lat': 'decimalLatitude', 'lon': 'decimalLongitude',
                                          'crs': 4326, 'sep': '\t'})

   #2 Этап — перепроецирование слоев в метрическую проекцию
   osm_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[osm_source])
   bio_reprojected = Preprocessor('reproject', params={'to': 'auto'}, from_actions=[bio_source])

   #3 Этап — объединяем данные в полигоны OSM (сопоставление методов) — важен порядок
   merged_vector = Merger('vector', params={'method': 'match', 'buffer': 10},
                          from_actions=[osm_reprojected, bio_reprojected])

   #4 Этап – расчет расстояний до объектов
   analysis = Analyzer('distance', params={'network_type': 'walk', 'visualize': True, 'color': 'green',
                                           'edgecolor': 'black', 'title': 'Parks with Quercus robur'},
                       from_actions=[merged_vector])

   #5 Этап – вывести все подготовленные выходные расчеты в консоль
   report = Report('stdout', from_actions=[analysis])

   # Запустить модель
   model = EstateModel().for_property(point_for_analysis, radius=2000)
   model.compose(report)

    
if __name__ == '__main__':
   launch_parks_with_quercus_proximity_analysis()