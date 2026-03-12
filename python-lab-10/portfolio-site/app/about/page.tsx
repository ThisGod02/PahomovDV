export default function AboutPage() {
    const skills = [
        "Frontend: React, Next.js, Vue.js, TypeScript",
        "Styles: CSS3, Tailwind CSS, SASS/SCSS",
        "Backend: Node.js, Express, Python",
        "Tools: Git, Vite, Webpack, Docker",
        "State: Redux, MobX, Context API"
    ];

    return (
        <div className="max-w-3xl mx-auto py-10 px-4">
            <h1 className="text-4xl font-extrabold mb-8 text-gray-900 border-b pb-4">Обо мне</h1>

            <div className="prose prose-blue lg:prose-xl text-gray-600 leading-relaxed mb-10">
                <p>Привет! Меня зовут Давид. Я увлекаюсь созданием современных веб-интерфейсов и постоянно изучаю новые технологии.</p>
                <p>Мой путь в веб-разработку начался с любопытства к тому, как работают сайты, и со временем это переросло в профессиональное призвание.</p>
            </div>

            <div className="grid gap-8">
                <section className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                    <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
                        <span className="text-blue-500">🛠</span> Навыки
                    </h2>
                    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {skills.map((skill, index) => (
                            <li key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl hover:bg-blue-50 transition-colors">
                                <span className="h-2 w-2 bg-blue-500 rounded-full"></span>
                                <span className="text-gray-700 font-medium">{skill}</span>
                            </li>
                        ))}
                    </ul>
                </section>

                <section className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                    <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
                        <span className="text-green-500">💼</span> Опыт работы
                    </h2>
                    <div className="space-y-8">
                        <div className="relative pl-8 border-l-2 border-green-200">
                            <span className="absolute -left-2.5 top-0 h-5 w-5 bg-green-500 rounded-full border-4 border-white"></span>
                            <h3 className="text-xl font-bold text-gray-800">Frontend Developer</h3>
                            <p className="text-sm font-semibold text-green-600 mb-2">2023 — Наст. время</p>
                            <p className="text-gray-600">Разработка и поддержка крупных корпоративных приложений на React. Оптимизация производительности и внедрение новых фич.</p>
                        </div>
                        <div className="relative pl-8 border-l-2 border-blue-200">
                            <span className="absolute -left-2.5 top-0 h-5 w-5 bg-blue-500 rounded-full border-4 border-white"></span>
                            <h3 className="text-xl font-bold text-gray-800">Junior Web Developer</h3>
                            <p className="text-sm font-semibold text-blue-600 mb-2">2022 — 2023</p>
                            <p className="text-gray-600">Создание лендингов, адаптивная верстка под все типы устройств. Работа с ванильным JavaScript и CSS препроцессорами.</p>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    )
}
