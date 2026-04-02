import React from 'react';
import MapView, { Marker } from 'react-native-maps';
import { StyleSheet, View } from 'react-native';

const NoteMap = ({ latitude, longitude, title }: any) => (
    <View style={styles.mapContainer}>
        <MapView
            style={styles.map}
            initialRegion={{
                latitude,
                longitude,
                latitudeDelta: 0.01,
                longitudeDelta: 0.01
            }}
        >
            <Marker coordinate={{ latitude, longitude }} title={title} />
        </MapView>
    </View>
);

const styles = StyleSheet.create({
    mapContainer: { height: 200, marginTop: 1, backgroundColor: 'white' },
    map: { flex: 1 }
});

export default NoteMap;
