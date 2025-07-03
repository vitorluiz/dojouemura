// src/hooks/useApi.js

import { useState, useEffect } from 'react';

/**
 * Hook customizado para gerenciar chamadas de API
 * @param {Function} apiFunction - Função que faz a chamada da API
 * @param {Array} dependencies - Dependências para reexecutar a chamada
 * @param {boolean} immediate - Se deve executar imediatamente
 */
export const useApi = (apiFunction, dependencies = [], immediate = true) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState(null);

  const execute = async (...args) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiFunction(...args);
      setData(result);
      return result;
    } catch (err) {
      setError(err);
      console.error('Erro na chamada da API:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (immediate) {
      execute();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencies);

  return {
    data,
    loading,
    error,
    execute,
    refetch: execute
  };
};

/**
 * Hook para gerenciar estado de formulários
 * @param {Object} initialValues - Valores iniciais do formulário
 * @param {Function} validationSchema - Função de validação
 */
export const useForm = (initialValues, validationSchema) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (name, value) => {
    setValues(prev => ({
      ...prev,
      [name]: value
    }));

    // Limpa o erro do campo quando o usuário começa a digitar
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null
      }));
    }
  };

  const handleBlur = (name) => {
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));

    // Valida o campo quando perde o foco
    if (validationSchema) {
      const fieldError = validationSchema(values, name);
      if (fieldError) {
        setErrors(prev => ({
          ...prev,
          [name]: fieldError
        }));
      }
    }
  };

  const validate = () => {
    if (!validationSchema) return true;

    const newErrors = validationSchema(values);
    setErrors(newErrors);
    
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (onSubmit) => {
    setIsSubmitting(true);
    
    // Marca todos os campos como tocados
    const allTouched = Object.keys(values).reduce((acc, key) => {
      acc[key] = true;
      return acc;
    }, {});
    setTouched(allTouched);

    try {
      if (validate()) {
        await onSubmit(values);
      }
    } catch (error) {
      console.error('Erro no envio do formulário:', error);
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    validate,
    reset,
    setValues,
    setErrors
  };
};

/**
 * Hook para gerenciar localStorage
 * @param {string} key - Chave do localStorage
 * @param {*} initialValue - Valor inicial
 */
export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Erro ao ler localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Erro ao salvar no localStorage key "${key}":`, error);
    }
  };

  const removeValue = () => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error(`Erro ao remover localStorage key "${key}":`, error);
    }
  };

  return [storedValue, setValue, removeValue];
};

