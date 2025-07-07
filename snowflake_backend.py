"""
Snowflake Backend for Celery

This module provides a custom Celery backend that uses Snowflake
instead of Redis for storing task results and managing the task queue.
"""

import json
import time
import uuid
from typing import Any, Dict, Optional
from celery.backends.base import BaseBackend
from time import monotonic
from snowflake_config import snowflake_manager
import logging

logger = logging.getLogger(__name__)

class SnowflakeBackend(BaseBackend):
    """
    Custom Celery backend that uses Snowflake for storing task results.
    """
    
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.snowflake = snowflake_manager
        
    def _get_task_key(self, task_id: str) -> str:
        """Generate a unique key for the task."""
        return f"task_{task_id}"
    
    def _serialize_result(self, result: Any) -> str:
        """Serialize result to JSON string."""
        try:
            return json.dumps(result)
        except (TypeError, ValueError) as e:
            logger.error(f"Error serializing result: {str(e)}")
            return json.dumps({"error": "Serialization failed", "original": str(result)})
    
    def _deserialize_result(self, result_str: str) -> Any:
        """Deserialize result from JSON string."""
        try:
            return json.loads(result_str)
        except (TypeError, ValueError) as e:
            logger.error(f"Error deserializing result: {str(e)}")
            return None
    
    def store_result(self, task_id: str, result: Any, state: str, 
                    traceback: Optional[str] = None, request: Optional[Dict] = None) -> None:
        """
        Store task result in Snowflake.
        
        Args:
            task_id (str): Unique task identifier
            result (Any): Task result
            state (str): Task state (SUCCESS, FAILURE, etc.)
            traceback (str, optional): Error traceback if task failed
            request (Dict, optional): Original task request
        """
        try:
            # Insert or update task result
            query = """
                INSERT INTO task_results (task_id, result_data, status, created_at, execution_time)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP(), %s)
                ON DUPLICATE KEY UPDATE
                    result_data = VALUES(result_data),
                    status = VALUES(status),
                    created_at = CURRENT_TIMESTAMP(),
                    execution_time = VALUES(execution_time)
            """
            
            result_data = self._serialize_result(result)
            execution_time = monotonic() if request else None
            
            self.snowflake.execute_query(query, (task_id, result_data, state, execution_time))
            
            logger.info(f"Stored result for task {task_id} with state {state}")
            
        except Exception as e:
            logger.error(f"Error storing result for task {task_id}: {str(e)}")
    
    def get_result(self, task_id: str) -> Optional[Any]:
        """
        Retrieve task result from Snowflake.
        
        Args:
            task_id (str): Unique task identifier
            
        Returns:
            Task result or None if not found
        """
        try:
            query = "SELECT result_data, status FROM task_results WHERE task_id = %s"
            cursor = self.snowflake.execute_query(query, (task_id,))
            row = cursor.fetchone()
            
            if row:
                result_data, status = row
                result = self._deserialize_result(result_data)
                logger.info(f"Retrieved result for task {task_id} with status {status}")
                return result
            else:
                logger.warning(f"No result found for task {task_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving result for task {task_id}: {str(e)}")
            return None
    
    def delete_result(self, task_id: str) -> None:
        """
        Delete task result from Snowflake.
        
        Args:
            task_id (str): Unique task identifier
        """
        try:
            query = "DELETE FROM task_results WHERE task_id = %s"
            self.snowflake.execute_query(query, (task_id,))
            logger.info(f"Deleted result for task {task_id}")
            
        except Exception as e:
            logger.error(f"Error deleting result for task {task_id}: {str(e)}")
    
    def cleanup(self) -> None:
        """Clean up old task results."""
        try:
            # Delete results older than 7 days
            query = """
                DELETE FROM task_results 
                WHERE created_at < DATEADD(day, -7, CURRENT_TIMESTAMP())
            """
            cursor = self.snowflake.execute_query(query)
            deleted_count = cursor.rowcount
            logger.info(f"Cleaned up {deleted_count} old task results")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    def _get_task_meta_for(self, task_id: str) -> Dict[str, Any]:
        """
        Get task metadata from Snowflake.
        This method is required by Celery.
        """
        try:
            query = """
                SELECT result_data, status, created_at, execution_time
                FROM task_results 
                WHERE task_id = %s
            """
            cursor = self.snowflake.execute_query(query, (task_id,))
            row = cursor.fetchone()
            
            if row:
                result_data, status, created_at, execution_time = row
                result = self._deserialize_result(result_data)
                
                meta = {
                    'task_id': task_id,
                    'status': status,
                    'result': result,
                    'date_done': created_at,
                    'traceback': None,
                    'children': [],
                    'parent_id': None,
                    'root_id': None,
                }
                
                if execution_time:
                    meta['runtime'] = execution_time
                
                return meta
            else:
                return {
                    'task_id': task_id,
                    'status': 'PENDING',
                    'result': None,
                    'date_done': None,
                    'traceback': None,
                    'children': [],
                    'parent_id': None,
                    'root_id': None,
                }
                
        except Exception as e:
            logger.error(f"Error getting task meta for {task_id}: {str(e)}")
            return {
                'task_id': task_id,
                'status': 'FAILURE',
                'result': None,
                'date_done': None,
                'traceback': str(e),
                'children': [],
                'parent_id': None,
                'root_id': None,
            }
    
    def get_task_meta(self, task_id: str) -> Dict[str, Any]:
        """
        Get task metadata. This is the main method called by Celery.
        """
        return self._get_task_meta_for(task_id)
    
    def _store_result(self, task_id: str, result: Any, state: str, 
                     traceback: Optional[str] = None, request: Optional[Dict] = None) -> None:
        """
        Store task result. This method is called by Celery.
        """
        self.store_result(task_id, result, state, traceback, request)
    
    def _delete_result(self, task_id: str) -> None:
        """
        Delete task result. This method is called by Celery.
        """
        self.delete_result(task_id)

class SnowflakeBroker:
    """
    Custom broker that uses Snowflake for task queue management.
    Note: This is a simplified implementation. In production, you might want
    to use a proper message broker like RabbitMQ or Apache Kafka.
    """
    
    def __init__(self):
        self.snowflake = snowflake_manager
    
    def enqueue_task(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """
        Add task to the queue.
        
        Args:
            task_name (str): Name of the task to execute
            task_data (Dict): Task parameters
            
        Returns:
            str: Task ID
        """
        task_id = str(uuid.uuid4())
        
        try:
            query = """
                INSERT INTO task_queue (task_id, task_name, task_data, status, created_at)
                VALUES (%s, %s, %s, 'PENDING', CURRENT_TIMESTAMP())
            """
            
            self.snowflake.execute_query(query, {
                'task_id': task_id,
                'task_name': task_name,
                'task_data': json.dumps(task_data)
            })
            
            logger.info(f"Enqueued task {task_id} ({task_name})")
            return task_id
            
        except Exception as e:
            logger.error(f"Error enqueueing task: {str(e)}")
            raise
    
    def dequeue_task(self) -> Optional[Dict[str, Any]]:
        """
        Get next task from the queue.
        
        Returns:
            Dict containing task information or None if queue is empty
        """
        try:
            # Get the oldest pending task
            query = """
                SELECT task_id, task_name, task_data, created_at
                FROM task_queue 
                WHERE status = 'PENDING'
                ORDER BY created_at ASC
                LIMIT 1
            """
            
            cursor = self.snowflake.execute_query(query)
            row = cursor.fetchone()
            
            if row:
                task_id, task_name, task_data, created_at = row
                
                # Mark task as processing
                update_query = """
                    UPDATE task_queue 
                    SET status = 'PROCESSING', updated_at = CURRENT_TIMESTAMP()
                    WHERE task_id = %s
                """
                self.snowflake.execute_query(update_query, {'task_id': task_id})
                
                return {
                    'task_id': task_id,
                    'task_name': task_name,
                    'task_data': json.loads(task_data),
                    'created_at': created_at
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error dequeuing task: {str(e)}")
            return None
    
    def mark_task_complete(self, task_id: str, status: str = 'COMPLETED') -> None:
        """
        Mark task as completed.
        
        Args:
            task_id (str): Task identifier
            status (str): Final status
        """
        try:
            query = """
                UPDATE task_queue 
                SET status = %s, updated_at = CURRENT_TIMESTAMP()
                WHERE task_id = %s
            """
            
            self.snowflake.execute_query(query, {
                'status': status,
                'task_id': task_id
            })
            
            logger.info(f"Marked task {task_id} as {status}")
            
        except Exception as e:
            logger.error(f"Error marking task {task_id} as {status}: {str(e)}")

# Global instances - these will be created when needed
# snowflake_backend = SnowflakeBackend()  # Removed to avoid instantiation error
snowflake_broker = SnowflakeBroker() 