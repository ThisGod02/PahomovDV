import React from 'react';
import { StyleSheet, View, Text } from 'react-native';

const NoteMap = ({ latitude, longitude, title }: any) => (
    <View style={styles.mapContainer}>
        <View style={styles.placeholder}>
            <Text style={styles.title}>Карта недоступна в веб-версии</Text>
            <Text style={styles.coords}>Координаты: {latitude.toFixed(4)}, {longitude.toFixed(4)}</Text>
        </View>
    </View>
);

const styles = StyleSheet.create({
    mapContainer: { height: 200, marginTop: 1, backgroundColor: '#f0f0f0' },
    placeholder: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
    title: { fontWeight: 'bold', marginBottom: 4 },
    coords: { color: '#007AFF' }
});

export default NoteMap;
