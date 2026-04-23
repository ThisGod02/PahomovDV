package com.example.expensetracker.models

import kotlinx.datetime.Instant

data class Category(
    val id: Long,
    val name: String,
    val color: String,
    val icon: String,
    val isDefault: Boolean = false
)

data class Expense(
    val id: Long,
    val amount: Double,
    val categoryId: Long,
    val description: String?,
    val date: Instant,
    val isSynced: Boolean = false
) {
    fun isValid(): Boolean = amount > 0

    fun formattedDate(): String = date.toString()
}

data class Budget(
    val id: Long,
    val categoryId: Long,
    val amount: Double,
    val month: Instant
) {
    fun remainingAmount(totalSpent: Double): Double = amount - totalSpent
    fun usagePercentage(totalSpent: Double): Double {
        if (amount <= 0) return 0.0
        return (totalSpent / amount).coerceIn(0.0, 1.0)
    }
}

// Статистика по категории
data class CategoryStats(
    val category: Category,
    val totalSpent: Double,
    val budget: Double?,
    val transactionCount: Int
) {
    val remainingBudget: Double?
        get() = budget?.let { it - totalSpent }

    val isOverBudget: Boolean
        get() = budget?.let { totalSpent > it } ?: false
}
