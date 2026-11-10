export default function OptionButtons({ options, onSelect, disabled }) {
  if (options.length === 0) return null;

  return (
    <div className="chat__options">
      {options.map((option) => (
        <button key={option} className="chat__option" onClick={() => onSelect(option)} disabled={disabled}>
          {option}
        </button>
      ))}
    </div>
  );
}
