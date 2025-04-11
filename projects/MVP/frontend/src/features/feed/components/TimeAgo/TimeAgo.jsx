import { HTMLAttributes, useEffect, useState } from "react";
import { timeAgo } from "../../utils/date";
import styles from "./TimeAgo.module.css";


export function TimeAgo({ date, edited, className, ...others }) {
  const [time, setTime] = useState(timeAgo(new Date(date)));

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(timeAgo(new Date(date)));
    }, 1000);

    return () => clearInterval(interval);
  }, [date]);

  return (
    <div className={`${styles.root} ${className ? className : ""}`} {...others}>
      <span>{time}</span>
      {/* {edited ? <span> . Edited</span> : <span></span>} */}
    </div>
  );
}