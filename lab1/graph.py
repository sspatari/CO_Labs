def get_station_graph():
    return station_graph

station_graph = {
                'eminescu' : { 'trolleybus_list' : [2,3,10,24], 'conn' : { 'kogalniceanu' : 2370 } } ,
               'kogalniceanu' : { 'trolleybus_list' : [2,3,10,24], 'conn' : { 'puskin' : 490,
                                                                     'casa_presei' : 1890} },
               'puskin' : { 'trolleybus_list' : [3], 'conn' : {} },
               'casa_presei' : { 'trolleybus_list' : [2,10,24], 'conn' : { 'mihai_eminescu_theatre' : 630,
                                                                  'stefan_cel_mare' : 1260 } },
               'mihai_eminescu_theatre' : { 'trolleybus_list' : [2], 'conn' : {} },
               'stefan_cel_mare' : { 'trolleybus_list' : [7,10,24,25], 'conn' : { 'asem' : 2240 } },
               'licurici' : { 'trolleybus_list' : [7,25], 'conn' : { 'stefan_cel_mare' : 980 } },
               'asem' : { 'trolleybus_list' : [7,10,24,25], 'conn' : { 'circul' : 2100 } },
               'circul' : { 'trolleybus_list' : [7,10,24,25], 'conn' : { 'central_typography' : 520,
                                                                'vladimirescu' : 300,
                                                                'kiev' : 1300} },
               'central_typography' : { 'trolleybus_list' : [25], 'conn' : {} },
               'vladimirescu' : { 'trolleybus_list' : [7], 'conn' : {} },
               'kiev' : { 'trolleybus_list' : [10,24], 'conn' : {} },
               }
