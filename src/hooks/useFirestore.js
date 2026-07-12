import { useState, useEffect } from 'react'
import {
  collection,
  query,
  orderBy,
  limit,
  onSnapshot,
  addDoc,
  serverTimestamp,
  where,
} from 'firebase/firestore'
import { db } from '../firebase/config'

/**
 * Listen to a Firestore collection in real-time.
 * @param {string} col - Collection name
 * @param {object} options - { orderByField, direction, limitCount, whereField, whereOp, whereValue }
 */
export function useCollection(col, options = {}) {
  const [docs, setDocs]     = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError]   = useState(null)

  useEffect(() => {
    let q = collection(db, col)
    const constraints = []

    if (options.whereField) {
      constraints.push(where(options.whereField, options.whereOp || '==', options.whereValue))
    }
    if (options.orderByField) {
      constraints.push(orderBy(options.orderByField, options.direction || 'desc'))
    }
    if (options.limitCount) {
      constraints.push(limit(options.limitCount))
    }

    q = query(q, ...constraints)

    const unsub = onSnapshot(
      q,
      (snap) => {
        const data = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() }))
        setDocs(data)
        setLoading(false)
      },
      (err) => {
        setError(err.message)
        setLoading(false)
      }
    )

    return () => unsub()
  }, [col])

  return { docs, loading, error }
}

/**
 * Add a document to a collection.
 */
export async function addDocument(col, data) {
  return addDoc(collection(db, col), {
    ...data,
    createdAt: serverTimestamp(),
  })
}
