import 'queue-microtask';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders welcome message', () => {
  render(<App />);
  const linkElement = screen.getByText(/Welcome to the Kikuyu Language Data Collection Interface/i);
  expect(linkElement).toBeInTheDocument();
});
