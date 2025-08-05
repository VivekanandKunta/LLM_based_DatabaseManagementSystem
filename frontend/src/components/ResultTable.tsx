"use client";

interface Props {
  data: any[];
}

export default function ResultTable({ data }: Props) {
  if (!Array.isArray(data) || data.length === 0) {
    return <div className="text-center mt-10 text-gray-500">No results to display.</div>;
  }

  const headers = Object.keys(data[0]);

  return (
    <div className="overflow-x-auto mt-10">
      <table className="table-auto w-full border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            {headers.map((header) => (
              <th key={header} className="px-4 py-2 border">{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-gray-50">
              {headers.map((header) => (
                <td key={header} className="px-4 py-2 border">{row[header]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
