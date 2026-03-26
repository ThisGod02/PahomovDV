export interface GeoNote {
    id: string;
    title: string;
    content: string;
    latitude: number;
    longitude: number;
    address?: string;
    photoUri?: string;
    createdAt: number; // timestamp
    updatedAt: number; // timestamp
}

export interface Location {
    latitude: number;
    longitude: number;
    address?: string;
}

export interface AppState {
    notes: GeoNote[];
    currentLocation: Location | null;
    isLoading: boolean;
    error: string | null;
}
