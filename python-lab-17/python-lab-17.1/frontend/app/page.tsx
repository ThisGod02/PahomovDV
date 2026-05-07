import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center animate-fade-in">
        <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight sm:text-6xl mb-6">
          Добро пожаловать в мое портфолио
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
          Я веб-разработчик, специализирующийся на современных технологиях. Создаю быстрые, надежные и красивые веб-приложения.
        </p>

        <div className="flex justify-center gap-4">
          <Link href="/projects" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition shadow-lg">
            Посмотреть проекты
          </Link>
          <Link href="/about" className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition shadow-sm">
            Подробнее обо мне
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition">
          <div className="h-12 w-12 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mb-6 text-2xl">⚡</div>
          <h2 className="text-2xl font-bold mb-3 text-gray-800">Next.js</h2>
          <p className="text-gray-600 leading-relaxed">Использование серверного рендеринга и статической генерации для максимальной производительности.</p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition">
          <div className="h-12 w-12 bg-green-100 text-green-600 rounded-lg flex items-center justify-center mb-6 text-2xl">⚛️</div>
          <h2 className="text-2xl font-bold mb-3 text-gray-800">React</h2>
          <p className="text-gray-600 leading-relaxed">Компонентный подход, декларативный UI и мощные хуки для сложной логики.</p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition">
          <div className="h-12 w-12 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center mb-6 text-2xl">🟦</div>
          <h2 className="text-2xl font-bold mb-3 text-gray-800">TypeScript</h2>
          <p className="text-gray-600 leading-relaxed">Строгая типизация для предотвращения ошибок и повышения качества кода.</p>
        </div>
      </div>
    </div>
  )
}
