// generate simple code for Card component

import React from 'react'

interface CardProps {
  title: string
  content: string
}

const Card: React.FC<CardProps> = ({ title, content }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div>{content}</div>
    </div>
  )
}
export default Card
