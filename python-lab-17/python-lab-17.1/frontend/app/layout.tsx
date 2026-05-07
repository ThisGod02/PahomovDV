import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin', 'cyrillic'] })

export const metadata: Metadata = {
  title: 'Мое портфолио',
  description: 'Сайт-портфолио разработчика',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={`${inter.className} min-h-screen flex flex-col bg-gray-50 text-gray-900`}>
        <header className="bg-gray-800 text-white shadow-md sticky top-0 z-10">
          <nav className="container mx-auto px-4 py-4">
            <div className="flex justify-between items-center">
              <Link href="/" className="text-xl font-bold tracking-tight">Портфолио</Link>
              <ul className="flex gap-8 font-medium">
                <li><Link href="/" className="hover:text-blue-400 transition-colors">Главная</Link></li>
                <li><Link href="/about" className="hover:text-blue-400 transition-colors">Обо мне</Link></li>
                <li><Link href="/blog" className="hover:text-blue-400 transition-colors">Блог</Link></li>
                <li><Link href="/projects" className="hover:text-blue-400 transition-colors">Проекты</Link></li>
              </ul>
            </div>
          </nav>
        </header>

        <main className="flex-grow container mx-auto px-4 py-8">
          {children}
        </main>

        <footer className="bg-gray-800 text-white py-8 border-t border-gray-700 mt-auto">
          <div className="container mx-auto px-4 text-center">
            <p className="text-gray-400">© 2026 Мое портфолио. Все права защищены.</p>
            <p className="mt-2 text-sm text-gray-500">Сделано с помощью Next.js и Tailwind CSS</p>
          </div>
        </footer>
      </body>
    </html>
  )
}
