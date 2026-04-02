package com.example.notesapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument
import com.example.notesapp.data.NoteDatabase
import com.example.notesapp.data.NoteRepository
import com.example.notesapp.ui.*

class MainActivity : ComponentActivity() {
    
    private lateinit var noteRepository: NoteRepository
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val database = NoteDatabase.getDatabase(this)
        noteRepository = NoteRepository(database.noteDao())
        
        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    NotesApp(noteRepository)
                }
            }
        }
    }
}

@Composable
fun NotesApp(noteRepository: NoteRepository) {
    val navController = rememberNavController()
    val viewModel: NotesViewModel = viewModel(
        factory = NotesViewModelFactory(noteRepository)
    )
    
    NavHost(
        navController = navController,
        startDestination = "notes_list"
    ) {
        composable("notes_list") {
            NotesScreen(
                viewModel = viewModel,
                onNoteClick = { noteId ->
                    navController.navigate("add_edit_note/$noteId")
                },
                onAddClick = {
                    navController.navigate("add_edit_note")
                }
            )
        }
        
        composable("add_edit_note") {
            AddEditNoteScreen(
                onSaveClick = { title, content ->
                    viewModel.addNote(title, content)
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
        
        composable(
            route = "add_edit_note/{noteId}",
            arguments = listOf(navArgument("noteId") { type = NavType.IntType })
        ) { backStackEntry ->
            val noteId = backStackEntry.arguments?.getInt("noteId") ?: 0
            LaunchedEffect(noteId) {
                viewModel.loadNoteById(noteId)
            }
            val note by viewModel.currentNote.collectAsState()
            
            if (note != null) {
                AddEditNoteScreen(
                    initialTitle = note!!.title,
                    initialContent = note!!.content,
                    onSaveClick = { title, content ->
                        viewModel.updateNote(noteId, title, content)
                    },
                    onNavigateBack = {
                        navController.popBackStack()
                    }
                )
            }
        }
    }
}
