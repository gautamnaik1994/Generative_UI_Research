import React, { Fragment } from 'react'

// Import necessary components
import Container from '../components/Container'
import Card from '../components/Card'
import Chart from '../components/Chart'

// ... import other components like Text, Image, List, Button etc.

const Renderer: FC<{ data: any }> = ({ data }) => {
  if (!data || !data.root) {
    return <h1>Loading...</h1>
  }

  const renderNode = (node: any) => {
    console.log('Rendering node:', node)

    switch (node.type) {
      case 'root':
        return (
          <>
            {node.children &&
              node.children.map((child: any, index: number) => (
                <Fragment key={index}>{renderNode(child)}</Fragment>
              ))}
          </>
        )
      case 'container':
        return (
          <Container direction={node.direction}>
            {node.children &&
              node.children.map((child: any, index: number) => (
                <Fragment key={index}>{renderNode(child)}</Fragment>
              ))}
          </Container>
        )
      case 'chart':
        return (
          <Chart
            dataKey={node.dataKey}
            x_axis={node.x_axis}
            y_axis={node.y_axis}
          ></Chart>
        )
      case 'card':
        return <Card title={node.title} content={node.content}></Card>
      case 'text':
        return <p className={node.variant}>{node.value}</p>
      case 'image':
        return <img src={node.src} alt={node.alt} />
      case 'list':
        return (
          <div className="list">
            {node.children &&
              node.children.map((item: any, index: number) => (
                <Fragment key={index}>{renderNode(item)}</Fragment>
              ))}
          </div>
        )
      case 'button':
        return (
          <button onClick={() => console.log(node.action)}>{node.label}</button>
        )

      default:
        return <pre>{JSON.stringify(node, null, 2)}</pre>
    }
  }
  // prevent rendering until data is available
  try {
    // debugger;
    // check if data.root exists
    // if (data.root && data.root.type === 'root' && data.root.children.length > 0) {
    // console.log('Rendering UI with data:', data)
    return <>{renderNode(data.root)}</>
    // }
  } catch (e) {
    return <h1>Loading...</h1>
  }
  // return <h1>Temp</h1>
}

export default Renderer
