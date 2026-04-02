// Веб-заглушка для базы данных, так как expo-sqlite не работает в браузере
import { GeoNote } from '../types';

export const initDatabase = (): Promise<void> => {
    console.log('Web version: Database initialization skipped');
    return Promise.resolve();
};

export const getNotes = (): Promise<GeoNote[]> => {
    console.log('Web version: Returning empty notes list');
    return Promise.resolve([]);
};

export const addNote = (note: GeoNote): Promise<void> => {
    console.log('Web version: Adding note ignored');
    return Promise.resolve();
};

export const deleteNote = (id: string): Promise<void> => {
    console.log('Web version: Deleting note ignored');
    return Promise.resolve();
};
