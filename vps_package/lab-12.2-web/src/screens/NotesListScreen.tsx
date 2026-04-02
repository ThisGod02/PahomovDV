import React, { useEffect } from 'react';
import {
    View,
    Text,
    FlatList,
    StyleSheet,
    TouchableOpacity,
    ActivityIndicator
} from 'react-native';
import { useAppDispatch, useAppSelector } from '../hooks/reduxHooks';
import { loadNotes } from '../store/notesSlice';

interface NotesListScreenProps {
    navigation: any;
}

const NotesListScreen: React.FC<NotesListScreenProps> = ({ navigation }) => {
    const dispatch = useAppDispatch();
    const { items: notes, loading, error } = useAppSelector(state => state.notes);

    useEffect(() => {
        dispatch(loadNotes());
    }, [dispatch]);

    const renderNoteItem = ({ item }: any) => (
        <TouchableOpacity
            style={styles.noteItem}
            onPress={() => navigation.navigate('NoteDetail', { noteId: item.id })}
        >
            <View style={styles.noteHeader}>
                <Text style={styles.noteTitle}>{item.title}</Text>
                <Text style={styles.noteDate}>
                    {new Date(item.createdAt).toLocaleDateString()}
                </Text>
            </View>
            <Text style={styles.noteContent} numberOfLines={2}>
                {item.content}
            </Text>
            {item.address && (
                <Text style={styles.noteAddress} numberOfLines={1}>
                    📍 {item.address}
                </Text>
            )}
        </TouchableOpacity>
    );

    if (loading && notes.length === 0) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#007AFF" />
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {notes.length === 0 ? (
                <View style={styles.emptyContainer}>
                    <Text style={styles.emptyText}>Нет заметок</Text>
                    <Text style={styles.emptySubtext}>
                        Нажмите + чтобы создать первую заметку
                    </Text>
                </View>
            ) : (
                <FlatList
                    data={notes}
                    renderItem={renderNoteItem}
                    keyExtractor={item => item.id}
                    contentContainerStyle={styles.listContent}
                />
            )}
            
            <TouchableOpacity
                style={styles.fab}
                onPress={() => navigation.navigate('AddNote')}
            >
                <Text style={styles.fabText}>+</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    centerContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    listContent: { padding: 16 },
    noteItem: {
        backgroundColor: 'white',
        borderRadius: 8,
        padding: 16,
        marginBottom: 12,
        elevation: 3
    },
    noteHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
    noteTitle: { fontSize: 16, fontWeight: 'bold', flex: 1 },
    noteDate: { fontSize: 12, color: '#666' },
    noteContent: { fontSize: 14, color: '#333', marginBottom: 8 },
    noteAddress: { fontSize: 12, color: '#007AFF' },
    emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 32 },
    emptyText: { fontSize: 20, fontWeight: 'bold', marginBottom: 8 },
    emptySubtext: { fontSize: 14, color: '#666', textAlign: 'center' },
    fab: {
        position: 'absolute',
        bottom: 24,
        right: 24,
        width: 56,
        height: 56,
        borderRadius: 28,
        backgroundColor: '#007AFF',
        justifyContent: 'center',
        alignItems: 'center',
        elevation: 8
    },
    fabText: { fontSize: 24, color: 'white', fontWeight: 'bold' }
});

export default NotesListScreen;
