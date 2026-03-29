export default function Footer() {
  return (
    <footer className="flex items-center justify-between px-6 py-6 bg-gray-100">
      <p className="text-sm text-gray-500">
        &copy; 2026 My Awesome Site. All rights reserved.
      </p>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md shadow-md">
        문의하기
      </button>
    </footer>
  );
}