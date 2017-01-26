google_map =                 '''<!DOCTYPE html>
        <html>
          <head>
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
            <meta charset="utf-8">
            <title>Simple markers</title>
            <style>
              html, body, #map-canvas {
                height: 100%;
                width: 100%
                margin: 0px;
                padding: 0px
              }
            </style>
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
            <script>

                var map;
                var markers = [];
                var results = [];
                var coords = [];
                var highestLevel;


                


                 function Marker(Lat,Lng) {
                  var Centre = new google.maps.LatLng(Lat,Lng);
                    var mapOptions = {
                    zoom: 2,
                    minZoom: 2,
                    center: Centre,
                    }
                map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions); 
                var mark = new google.maps.LatLng(Lat,Lng);
                //return Skatepark;

                AddMarker(mark); }




                function AddMarker(location) {


                var marker = new google.maps.Marker({
                title: 'Test',
                position: location,
                animation: google.maps.Animation.DROP,
                map: map

                });
                //markers.push(marker);
                var lat = marker.getPosition().lat();
                var lng = marker.getPosition().lng();
                markers.push({"Object":marker,"Lat":lat,"Lng":lng});

                        var contentString = '<div id="content">'+
              '<div id="siteNotice">'+
              '</div>'+
              '<h1 id="firstHeading" class="firstHeading">Alert</h1>'+
              '<div id="bodyContent">'+
              '<p>Location encoded in message</p>'+
              '</div>'+
              '</div>';

              var infowindow = new google.maps.InfoWindow({
              content: contentString
          });

              google.maps.event.addListener(marker, 'rightclick', function(event) {
                marker.setMap(null);
                });
            google.maps.event.addListener(marker, 'mouseover', function(event) {
            infowindow.open(map,marker);
          });
               }


        function GetMarkers(){
             return markers;
                }


        
            </script>
          </head>
          <body>
            <div id="map-canvas"></div>
          </body>
        </html> '''


blank =                 '''<!DOCTYPE html>
        <html>
       <body>

        <h1>No Map</h1>

        <p>No Map Data.</p>

        </body>
        </html> '''
