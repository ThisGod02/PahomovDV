package com.example.expensetracker.viewmodels

import com.example.expensetracker.db.Database
import com.example.expensetracker.models.Category
import com.example.expensetracker.models.Expense
import com.example.expensetracker.models.CategoryStats
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlinx.datetime.*

class ExpensesViewModel(private val database: Database) {
    private val viewModelScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    private val _state = MutableStateFlow(ExpensesState())
    val state: StateFlow<ExpensesState> = _state.asStateFlow()
    
    private var _currentMonth = MutableStateFlow(LocalDate(Clock.System.todayIn(TimeZone.currentSystemDefault()).year, Clock.System.todayIn(TimeZone.currentSystemDefault()).monthNumber, 1))

    init {
        loadData()
    }

    private fun loadData() {
        _currentMonth.flatMapLatest { date ->
            combine(
                database.getAllCategories(),
                database.getExpensesForMonth(date.year, date.monthNumber),
                database.getBudgetForMonth(date.year, date.monthNumber)
            ) { categories, expenses, budgets ->
                _state.update { it.copy(categories = categories, expenses = expenses, budgets = budgets, isLoading = false) }
            }
        }.launchIn(viewModelScope)
    }

    fun addExpense(amount: Double, categoryId: Long, description: String?) {
        viewModelScope.launch {
            database.insertExpense(Expense(0, amount, categoryId, description, Clock.System.now()))
        }
    }

    fun calculateCategoryStats(): List<CategoryStats> {
        val s = state.value
        return s.categories.map { category ->
            val spent = s.expenses.filter { it.categoryId == category.id }.sumOf { it.amount }
            val budget = s.budgets.find { it.categoryId == category.id }?.amount
            CategoryStats(category, spent, budget, s.expenses.count { it.categoryId == category.id })
        }
    }
}

data class ExpensesState(
    val categories: List<Category> = emptyList(),
    val expenses: List<Expense> = emptyList(),
    val budgets: List<any> = emptyList(), // Simplified for example
    val isLoading: Boolean = true,
    val error: String? = null
)
