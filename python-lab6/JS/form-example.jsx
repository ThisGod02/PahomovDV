// Пример использования кастомного хука useForm
import React from 'react';
import { useForm } from './react-functional.js';

const LoginForm = () => {
    const {
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        handleSubmit,
        setFieldValue
    } = useForm({
        email: '',
        password: ''
    });

    const validationRules = {
        email: {
            required: 'Email обязателен',
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            patternMessage: 'Некорректный формат email'
        },
        password: {
            required: 'Пароль обязателен',
            validator: (value) => {
                if (value.length < 6) {
                    return 'Пароль должен содержать минимум 6 символов';
                }
                return null;
            }
        }
    };

    const onSubmit = (formValues) => {
        console.log('Форма отправлена:', formValues);
        alert(`Вход выполнен для: ${formValues.email}`);
    };

    return (
        <form onSubmit={handleSubmit(onSubmit, validationRules)}>
            <div>
                <label>Email:</label>
                <input
                    type="email"
                    name="email"
                    value={values.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    onBlur={() => handleBlur('email')}
                />
                {touched.email && errors.email && (
                    <span style={{ color: 'red' }}>{errors.email}</span>
                )}
            </div>

            <div>
                <label>Пароль:</label>
                <input
                    type="password"
                    name="password"
                    value={values.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    onBlur={() => handleBlur('password')}
                />
                {touched.password && errors.password && (
                    <span style={{ color: 'red' }}>{errors.password}</span>
                )}
            </div>

            <button type="submit">Войти</button>
        </form>
    );
};

export default LoginForm;


