import Link from 'next/link'
import { blogPosts } from './data'

export default function BlogPage() {
    return (
        <div className="max-w-5xl mx-auto py-10 px-4">
            <h1 className="text-4xl font-extrabold mb-10 text-gray-900 border-b pb-4">Блог</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {blogPosts.map((post) => (
                    <article key={post.id} className="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300 flex flex-col">
                        <div className="p-8 flex-grow">
                            <div className="flex items-center gap-2 text-sm text-blue-600 font-semibold mb-4 uppercase tracking-wider">
                                <span>Разработка</span>
                                <span className="h-1 w-1 bg-blue-600 rounded-full"></span>
                                <span>{post.date}</span>
                            </div>
                            <h2 className="text-2xl font-bold mb-4 text-gray-800 group-hover:text-blue-600 transition-colors">
                                <Link href={`/blog/${post.slug}`}>
                                    {post.title}
                                </Link>
                            </h2>
                            <p className="text-gray-600 leading-relaxed mb-6 line-clamp-3">
                                {post.excerpt}
                            </p>
                        </div>
                        <div className="px-8 py-5 bg-gray-50 border-t border-gray-100 flex justify-between items-center text-sm">
                            <span className="font-medium text-gray-700">Автор: {post.author}</span>
                            <Link href={`/blog/${post.slug}`} className="text-blue-600 font-bold flex items-center gap-1 hover:gap-2 transition-all">
                                Читать полностью <span>→</span>
                            </Link>
                        </div>
                    </article>
                ))}
            </div>
        </div>
    )
}
