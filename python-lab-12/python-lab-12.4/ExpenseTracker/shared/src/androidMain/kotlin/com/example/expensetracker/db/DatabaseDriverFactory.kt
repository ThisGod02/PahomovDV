package com.example.expensetracker.db

import android.content.Context
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.android.AndroidSqliteDriver
import com.example.expensetracker.ExpenseDatabase

actual class DatabaseDriverFactory(
    private val context: Context
) {
    actual fun createDriver(): SqlDriver {
        return AndroidSqliteDriver(
            schema = ExpenseDatabase.Schema,
            name = "expense.db",
            context = context
        )
    }
}
