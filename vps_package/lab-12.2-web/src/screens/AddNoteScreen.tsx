import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    TextInput,
    StyleSheet,
    TouchableOpacity,
    ScrollView,
    Alert,
    ActivityIndicator,
    Image
} from 'react-native';
import * as Location from 'expo-location';
import * as ImagePicker from 'expo-image-picker';
import { useAppDispatch } from '../hooks/reduxHooks';
import { saveNote } from '../store/notesSlice';
import { GeoNote } from '../types';
import { Platform } from 'react-native';

if (Platform.OS !== 'web') {
    require('react-native-get-random-values');
}
import { v4 as uuidv4 } from 'uuid';

interface AddNoteScreenProps {
    navigation: any;
}

const AddNoteScreen: React.FC<AddNoteScreenProps> = ({ navigation }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [address, setAddress] = useState<string | undefined>();
    const [photoUri, setPhotoUri] = useState<string | undefined>();
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
    
    const dispatch = useAppDispatch();

    useEffect(() => {
        getCurrentLocation();
    }, []);

    const getCurrentLocation = async () => {
        setIsLoading(true);
        try {
            const { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Ошибка', 'Нет доступа к геолокации');
                return;
            }

            const currentLocation = await Location.getCurrentPositionAsync({});
            setLocation({
                latitude: currentLocation.coords.latitude,
                longitude: currentLocation.coords.longitude
            });

            const addresses = await Location.reverseGeocodeAsync({
                latitude: currentLocation.coords.latitude,
                longitude: currentLocation.coords.longitude
            });

            if (addresses.length > 0) {
                const addr = addresses[0];
                const addressString = [addr.street, addr.city, addr.country].filter(Boolean).join(', ');
                setAddress(addressString);
            }
        } catch (error) {
            Alert.alert('Ошибка', 'Не удалось получить местоположение');
        } finally {
            setIsLoading(false);
        }
    };

    const takePhoto = async () => {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') {
            Alert.alert('Ошибка', 'Нет доступа к камере');
            return;
        }

        const result = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            quality: 0.7
        });

        if (!result.canceled) {
            setPhotoUri(result.assets[0].uri);
        }
    };

    const handleSave = async () => {
        if (!title || !content || !location) return;

        setIsSaving(true);
        const newNote: GeoNote = {
            id: uuidv4(),
            title,
            content,
            latitude: location.latitude,
            longitude: location.longitude,
            address,
            photoUri,
            createdAt: Date.now()
        };

        try {
            await dispatch(saveNote(newNote)).unwrap();
            navigation.goBack();
        } catch (error) {
            Alert.alert('Ошибка', 'Не удалось сохранить заметку');
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.form}>
                <Text style={styles.label}>Заголовок</Text>
                <TextInput style={styles.input} value={title} onChangeText={setTitle} />

                <Text style={styles.label}>Содержание</Text>
                <TextInput style={[styles.input, styles.textArea]} value={content} onChangeText={setContent} multiline />

                <View style={styles.section}>
                    <Text style={styles.label}>📍 Местоположение</Text>
                    {isLoading ? <ActivityIndicator color="#007AFF" /> : <Text>{address || 'Определяется...'}</Text>}
                </View>

                <TouchableOpacity style={styles.button} onPress={takePhoto}>
                    <Text style={styles.buttonText}>{photoUri ? '📸 Фото добавлено' : '📷 Сделать фото'}</Text>
                </TouchableOpacity>

                {photoUri && <Image source={{ uri: photoUri }} style={styles.preview} />}

                <TouchableOpacity 
                    style={[styles.saveButton, (!title || !content || !location || isSaving) && styles.disabled]} 
                    onPress={handleSave}
                    disabled={!title || !content || !location || isSaving}
                >
                    {isSaving ? <ActivityIndicator color="white" /> : <Text style={styles.saveButtonText}>Сохранить</Text>}
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: 'white' },
    form: { padding: 20 },
    label: { fontSize: 16, fontWeight: 'bold', marginBottom: 8 },
    input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, marginBottom: 16 },
    textArea: { height: 100, textAlignVertical: 'top' },
    section: { marginBottom: 16 },
    button: { backgroundColor: '#e1f5fe', padding: 12, borderRadius: 8, alignItems: 'center', marginBottom: 12 },
    buttonText: { color: '#007AFF', fontWeight: 'bold' },
    preview: { width: '100%', height: 200, borderRadius: 8, marginBottom: 16 },
    saveButton: { backgroundColor: '#007AFF', padding: 16, borderRadius: 8, alignItems: 'center' },
    saveButtonText: { color: 'white', fontWeight: 'bold', fontSize: 16 },
    disabled: { backgroundColor: '#ccc' }
});

export default AddNoteScreen;
