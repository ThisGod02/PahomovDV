package com.example.expensetracker.models

import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable

@Serializable
data class Category(
    val id: Long,
    val name: String,
    val color: String,
    val icon: String,
    val isDefault: Boolean = false
)

@Serializable
data class Expense(
    val id: Long,
    val amount: Double,
    val categoryId: Long,
    val description: String?,
    val date: Instant,
    val isSynced: Boolean = false
) {
    fun isValid(): Boolean = amount > 0
    fun formattedDate(): String = date.toString() // Placeholder
}

data class CategoryStats(
    val category: Category,
    val totalSpent: Double,
    val budget: Double?,
    val transactionCount: Int
)
