// This example requires ECharts v5.4.0 or later
myChart.showLoading();
$.get(ROOT_PATH + '/data/asset/geo/USA.json', function (usaJson) {
  echarts.registerMap('USA', usaJson);

const locations = [
    { name: "485 Granite St, Braintree, MA", value: [-70.9995, 42.2079] },
    { name: "376 Arsenal St, Watertown, MA", value: [-71.1596, 42.3626] },
    { name: "129 Turnpike St, North Andover, MA", value: [-71.1028, 42.6334] },
    { name: "1398 Massachusetts Ave, Arlington, MA", value: [-71.1569, 42.4098] },
    { name: "380R Merrimack St, Methuen, MA", value: [-71.1796, 42.7262] },
    { name: "50 Dodge Street, Beverly, MA", value: [-70.8887, 42.5584] },
    { name: "45 Drum Hill Rd, Chelmsford, MA", value: [-71.3673, 42.6195] },
    { name: "450 Paradise Rd, Swampscott, MA", value: [-70.9174, 42.4745] },
    { name: "3 Flagstone Dr, Hudson, NH", value: [-71.4403, 42.7646] },
    { name: "296 Main St, Haverhill, MA", value: [-71.0825, 42.7735] },
    { name: "359 N Central Avenue, Hartsdale, NY", value: [-73.7989, 41.0212] },
    { name: "161 Boston Ave, Bridgeport, CT", value: [-73.1815, 41.1914] },
    { name: "3379 Crompond Rd, Yorktown Heights, NY", value: [-73.8294, 41.2943] },
    { name: "1918 Black Rock Turnpike, Fairfield, CT", value: [-73.2413, 41.1869] },
    { name: "389 Bridgeport Avenue, Shelton, CT", value: [-73.1285, 41.2726] },
    { name: "4200 Main Street, Bridgeport, CT", value: [-73.2075, 41.2076] },
    { name: "203 Gramatan Ave, Ste A, Mt Vernon, NY", value: [-73.8365, 40.9175] },
    { name: "5 N Airmont Rd, #4, Airmont, NY", value: [-74.0995, 41.1168] },
    { name: "42 Rockland Plaza, Ste 22, Nanuet, NY", value: [-74.0155, 41.0951] },
    { name: "57 Monroe Turnpike, Trumbull, CT", value: [-73.2061, 41.2562] },
    { name: "527 Elm St, New Haven, CT", value: [-72.9275, 41.3108] },
    { name: "50 Westchester Avenue, Port Chester, NY", value: [-73.6657, 41.0018] },
    { name: "1874B Route 6, Carmel, NY", value: [-73.6785, 41.3987] },
    { name: "777 White Plains Road, Scarsdale, NY", value: [-73.8166, 41.0155] },
    { name: "843 Hutchinson River Parkway, Bronx, NY", value: [-73.8283, 40.8288] },
    { name: "1210 Webster Ave, Bronx, NY", value: [-73.9073, 40.8316] },
    { name: "5546 Broadway, Bronx, NY", value: [-73.8998, 40.8770] },
    { name: "332 E 149th Street, Bronx, NY", value: [-73.9182, 40.8164] },
    { name: "2128 Rockaway Parkway, Brooklyn, NY", value: [-73.9027, 40.6377] },
    { name: "233-15 Hillside Ave, Queens Village, NY", value: [-73.7340, 40.7268] },
    { name: "2310 Hempstead Turnpike, East Meadow, NY", value: [-73.5571, 40.7261] },
    { name: "125 Sunrise Hwy, West Islip, NY", value: [-73.2997, 40.7079] },
    { name: "1037 Fulton St, Farmingdale, NY", value: [-73.4456, 40.7326] },
    { name: "24 Railroad Ave, Patchogue, NY", value: [-73.0153, 40.7642] },
    { name: "1585 Dutch Broadway, Valley Stream, NY", value: [-73.7004, 40.6827] },
    { name: "13337 41st Ave, Ste B, Flushing, NY", value: [-73.8322, 40.7590] },
    { name: "13525 79th St, Unit G, Howard Beach, NY", value: [-73.8480, 40.6574] },
    { name: "464 Atlantic Avenue, East Rockaway, NY", value: [-73.6709, 40.6426] },
    { name: "213-04 Northern Blvd, Queens, NY", value: [-73.7669, 40.7597] },
    { name: "3400 Boston Road, Bronx, NY", value: [-73.8546, 40.8722] },
    { name: "352 Ryders Lane, Milltown, NJ", value: [-74.4286, 40.4438] },
    { name: "1120 Route 9 South, Old Bridge, NJ", value: [-74.3259, 40.3853] },
    { name: "802 Pleasant Drive, Rockville, MD", value: [-77.1506, 39.0897] },
    { name: "2501 E Hallandale Beach Blvd, Hallandale Beach, FL", value: [-80.1436, 25.9861] },
    { name: "5475 Poplar Ave #106, Memphis, TN", value: [-89.8735, 35.1056] },
    { name: "7570 Voice of America Centre Dr, West Chester, OH", value: [-84.3646, 39.3619] },
    { name: "3714 Madison Road, Cincinnati, OH", value: [-84.4231, 39.1568] },
    { name: "980 Plainfield Rd, Willowbrook, IL", value: [-87.9391, 41.7558] },
    { name: "1355 E Ogden Ave, Naperville, IL", value: [-88.1173, 41.7850] },
    { name: "4004 N 132nd St #101, Omaha, NE", value: [-96.1183, 41.2985] },
    { name: "465 S Mount Auburn Rd, Ste 103, Cape Girardeau, MO", value: [-89.5685, 37.2976] },
    { name: "3161 N Rock Rd, Suite A, Wichita, KS", value: [-97.2436, 37.7385] },
    { name: "320 Geneva Ave, Joplin, MO", value: [-94.5133, 37.0842] },
    { name: "10850 Louetta Road, Ste 1500, Houston, TX", value: [-95.5805, 30.0122] },
    { name: "107 Yale St, Ste 200, Houston, TX", value: [-95.3982, 29.7725] },
    { name: "1921 League City Parkway, League City, TX", value: [-95.0857, 29.4845] },
    { name: "3551 Hwy 6, Sugarland, TX", value: [-95.6110, 29.5926] },
    { name: "1335 E South Boulder Rd, Louisville, CO", value: [-105.1272, 39.9860] },
    { name: "2795 Pearl St, Boulder, CO", value: [-105.2595, 40.0220] },
    { name: "2804 South Timberline, Fort Collins, CO", value: [-105.0380, 40.5401] }
];

  option = {
    geo: {
      map: 'USA',
      roam: true,
      itemStyle: {
        areaColor: '#e7e8ea'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}'
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'geo',
        data: locations,
        symbolSize: 8,
        label: {
          show: false
        },
        itemStyle: {
          color: 'red'
        }
      }
    ]
  };

  myChart.hideLoading();
  myChart.setOption(option);
});
