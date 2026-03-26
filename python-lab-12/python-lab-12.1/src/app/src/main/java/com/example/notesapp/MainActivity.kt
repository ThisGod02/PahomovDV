package com.example.notesapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.notesapp.data.NoteDatabase
import com.example.notesapp.data.NoteRepository
import com.example.notesapp.ui.AddEditNoteScreen
import com.example.notesapp.ui.NotesScreen
import com.example.notesapp.ui.NotesViewModel
import com.example.notesapp.ui.NotesViewModelFactory
import com.example.notesapp.ui.theme.NotesAppTheme

class MainActivity : ComponentActivity() {
    
    private lateinit var noteRepository: NoteRepository
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val database = NoteDatabase.getDatabase(this)
        noteRepository = NoteRepository(database.noteDao())
        
        setContent {
            NotesAppTheme {
                NotesApp(noteRepository)
            }
        }
    }
}

@Composable
fun NotesApp(noteRepository: NoteRepository) {
    val navController = rememberNavController()
    
    NavHost(
        navController = navController,
        startDestination = "notes_list"
    ) {
        composable("notes_list") {
            NotesScreen(
                viewModel = viewModel(
                    factory = NotesViewModelFactory(noteRepository)
                ),
                onNoteClick = { noteId ->
                    navController.navigate("add_edit_note/$noteId")
                },
                onAddClick = {
                    navController.navigate("add_edit_note")
                }
            )
        }
        
        composable("add_edit_note") {
            val vm: NotesViewModel = viewModel(factory = NotesViewModelFactory(noteRepository))
            AddEditNoteScreen(
                onSaveClick = { title, content ->
                    vm.addNote(title, content)
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
        
        composable("add_edit_note/{noteId}") { backStackEntry ->
            val noteId = backStackEntry.arguments?.getString("noteId")?.toInt() ?: 0
            val vm: NotesViewModel = viewModel(factory = NotesViewModelFactory(noteRepository))
            
            LaunchedEffect(noteId) {
                vm.loadNoteById(noteId)
            }
            
            val note by vm.currentNote.collectAsState()
            
            if (note != null) {
                AddEditNoteScreen(
                    initialTitle = note!!.title,
                    initialContent = note!!.content,
                    onSaveClick = { title, content ->
                        vm.updateNote(noteId, title, content)
                    },
                    onNavigateBack = {
                        navController.popBackStack()
                    }
                )
            }
        }
    }
}
