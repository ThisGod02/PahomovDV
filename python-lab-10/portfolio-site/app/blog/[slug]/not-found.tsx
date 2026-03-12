import Link from 'next/link'

export default function NotFound() {
    return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4">
            <div className="text-8xl mb-8 animate-bounce">🔍</div>
            <h1 className="text-5xl font-extrabold text-gray-900 mb-4 tracking-tighter">Статья не найдена</h1>
            <p className="text-xl text-gray-600 mb-10 max-w-md mx-auto leading-relaxed">
                К сожалению, статья, которую вы ищете, не существует или была перенесена в другое место.
            </p>
            <Link
                href="/blog"
                className="inline-flex items-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-2xl font-bold hover:bg-blue-700 transition shadow-lg hover:shadow-xl active:scale-95"
            >
                <span>←</span> Вернуться к блогу
            </Link>
        </div>
    )
}
